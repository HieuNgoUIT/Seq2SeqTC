# This project is the testset generator

## Table of contents

- [1. Cấu trúc File](#cấu-trúc-file)
- [2. Setup môi trường](#setup-môi-trường)
- [3. Triển khai API](#triển-khai-api)

## Cấu trúc file

    api-testset-generator/
        api.py                              => File chạy API
        Components/                         => Module chứa các components cần thiết
            generator_number.py             => Tạo testset dưa trên số lượng xác định
            generator_ratio.py              => Tạo testset dưa trên tỉ lệ xác định
            preprocess.py                   => Tiền xử lý đầu vào
            acronym.py                      => Tạo lỗi viêt tắt
            edit_distance.py                => Tạo lỗi edit distance
            fat_finger.py                   => Tạo lỗi fat finger
            region.py                       => Tạo lỗi vùng miền
            region_new.py                   => Tạo lỗi vùng miền (đã câp nhật)
            teencode.py                     => Tạo lỗi teencode
            telex.py                        => Tạo lỗi telex
        templates/                          => Khung giao diện chính của trang web 
        
## Setup môi trường

    - conda create -y --name text_correction python=3.7
    - pip3 install -r requirements.txt  

## Triển khai api:

    - python3 api.py