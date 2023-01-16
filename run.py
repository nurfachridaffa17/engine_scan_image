import ktp_image as ktpg
from genericpath import exists
import entity as extractor
import kyc_config as cfg
import ocr_gcloud as ocr
import os
import pandas as pd


def list_files():
    image_path = []
    for path in os.listdir('data_ktp'):
    # check if current path is a file
        if os.path.isfile(os.path.join('data_ktp', path)):
            image_path.append(path)
    return image_path


def data_ktp():
    data_img = []
    img_data = 'data_ktp/{}'
    length = 0
    for img in list_files():
        img_path = img_data.format(img)
        ocr.process_ocr(img_path)
        img_name = img_path.split('/')[-1].split('.')[0]
        ocr_path = cfg.json_loc+'ocr_'+img_name+'.npy'
        data_ktp = extractor.process_extract_entities(ocr_path).to_dict(orient='records')

        if length <= len(list_files()):
            length += 1

        data = {
            'id' :length,
            'id_user': 'null',
            'jenis_kelamin': data_ktp[0]['gender'], 
            'id_kawin': data_ktp[0]['marital_status'], 
            'id_status': 'null', 
            'id_pekerjaan': data_ktp[0]['occupation'], 
            'id_struktur': 'null', 
            'id_agama': data_ktp[0]['religion'], 
            'id_organisasi': 'null', 
            'kode_member': 'null', 
            'nik': data_ktp[0]['identity_number'], 
            'nama': data_ktp[0]['fullname'], 
            'tempat_lahir': data_ktp[0]['birth_place'], 
            'tanggal_lahir': data_ktp[0]['birth_date'], 
            'jabatan': 'null', 
            'no_hp': 'null', 
            'is_hp_verified': 'null', 
            'email': 'null', 
            'alamat_domisili': data_ktp[0]['address'], 
            'alamat_ktp': data_ktp[0]['address'], 
            'desc': 'null', 
            'created': 'null', 
            'createdby': 1, 
            'updated': 'null', 
            'updatedby': 1, 
            'isactive': 'null', 
            'id_kategori': 'null'
            }
        
        if data_ktp[0]['gender'] == 'Male':
            data['jenis_kelamin'] = 1
        else:
            data['jenis_kelamin'] = 2
        
        if data_ktp[0]['occupation'] == 'Mengurus Rumah Tangga':
            data['id_pekerjaan'] = 1
        elif data_ktp[0]['occupation'] == 'Buruh Harian Lepas':
            data['id_pekerjaan'] = 2
        elif data_ktp[0]['occupation'] == 'Pegawai Negeri Sipil':
            data['id_pekerjaan'] = 3
        elif data_ktp[0]['occupation'] == 'Pelajar/Mahasiswa':
            data['id_pekerjaan'] = 4
        elif data_ktp[0]['occupation'] == 'Karyawan Swasta':
            data['id_pekerjaan'] = 5
        elif data_ktp[0]['occupation'] == 'Pegawai Negeri':
            data['id_pekerjaan'] = 6
        elif data_ktp[0]['occupation'] == 'Wiraswasta':
            data['id_pekerjaan'] = 7
        else :
            data['id_pekerjaan'] = 8

        if data_ktp[0]['marital_status'] == 'Single':
            data['id_kawin'] = 1
        elif data_ktp[0]['marital_status'] == 'Married':
            data['id_kawin'] = 2
        elif data_ktp[0]['marital_status'] == 'Cerai Hidup':
            data['id_kawin'] = 3
        else:
            data['id_kawin'] = 4
        
        if data_ktp[0]['religion'] == 'ISLAM':
            data['id_agama'] = 1
        else:
            data['id_agama'] = 1

        data_img.append(data)
        

    df = pd.DataFrame(data_img)

    if df.empty:
        print("DataFrame is empty.")
    else:
        print("DataFrame has data.")
        df.to_csv('data_ktp_4.csv', header=True, index=False, na_rep='null')


list_files()
data_ktp()