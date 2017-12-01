#!/bin/bash

echo "Ladder Needed!"

if [ ! -d ~/data/imagenet ];then
    mkdir -p ~/data/imagenet
fi
cd ~/data/imagenet

# object detction
imagenet_od_train="https://storage.googleapis.com/kaggle-competitions-data/kaggle/6796/imagenet_object_detection_train.tar.gz?GoogleAccessId=competitions-data@kaggle-161607.iam.gserviceaccount.com&Expires=1504351888&Signature=gCrPsHlkiPXiiATb5hz69aOEcQhLHERdI%2BwbEZnkob86gcbEUVDEHryiuvpTazFPjd0b74uaEgAdeCMAL%2FoOUReevqNLgEW1606Ygw6%2BKJggGYrc5IuY7BQaDLhj5PgyprHEaPG8Z2uQwg8nMrnWxaupwylCFykQhwtErdKHoImrdSsTt771Zodhuwzy3pWoLGv27aRLIcmgunJBgeeqvZKsGGuSWdB3Bxhlr%2BBEGoZ6rdZDcARP8145xOwvl2%2FuQv8CZeaiZKpGJqMdZN4F4uWAmZX4hY3NMNgCMvWX8JmNXzfTknSrqjizspfu0zsFT7QiexiRKaNdcoH%2BZOkOBw%3D%3D"

imagenet_od_test="https://storage.googleapis.com/kaggle-competitions-data/kaggle/6796/imagenet_object_detection_test.tar.gz?GoogleAccessId=competitions-data@kaggle-161607.iam.gserviceaccount.com&Expires=1504351893&Signature=lX9yNzli8R91na%2BfqEO%2B0cbtqYTKj66WTTd1sDuHLa6tnIMTQHlS9WF4%2FVnxPYNugnSYEoFw1G7wMVvHUZU3t6FZWoWK0xUpQqujGwlJJbM%2F23KFFUQIGGzPCwcjiT9s9U7yEM4jmRWsniTnqGaOZl7G3soxXO%2FVLXTjx88A4ZUr9pPaHUKk%2FuZu5hMLw2XRwNRGXX8QxsyFAc%2Fk3KaSWQ8o9V9ZAr8QNffkImAPfP6yCmFXx8rEwS9fcbTdaEzoILTPymmOR5rBCiZiSNuwu6shDBke0dAde%2BeNQBCidVzEc2IpQonmu62Yuc%2Fx3iAPXKgY7R1gAJSqzwCcPQLYEQ%3D%3D"


# object localization
imagenet_loc="https://storage.googleapis.com/kaggle-competitions-data/kaggle/6799/imagenet_object_localization.tar.gz?GoogleAccessId=competitions-data@kaggle-161607.iam.gserviceaccount.com&Expires=1504345709&Signature=lCQ6grJg8guTpdnV0TI3BCiOoeiXzHfAz6pAyh14WRlk%2BqmSwfSC611aLXVKYU79NpK7k1p%2BxM7QqioLsWNn1zne3wlqVWv8y2xZ1oUcfJytf4G1RlhlowgMbiR4nCzVlq31NjjgATx4bE5gOkNZNxtNPKbdHMWv5ZyKRQnlwfvgN03bSK7IBmkS%2BlpD5I0EGcK0lLWdQA6ndlg45Evav%2B5%2ByT0BROnKuKou1l8LWeINXKA7NLGBLdoxcGa9aCoLjjTMBkMAyDqpqcET2zH4IshBYCrFRH9fTL2d7iFkFik5ms5p4nJd2Ph%2BDk5OtQYdjuegHBPO54W0HcuhAyIpXQ%3D%3D"

wget $imagenet_od_train -O imagenet_object_detection_train.tar.gz
wget $imagenet_od_test -O imagenet_object_detection_test.tar.gz
wget $imagenet_loc -O imagenet_localization.tar.gz

for i in `ls *.tar.gz`;do
    tar -zxvf $i
done

echo "Imagenet for detection and localization are saved in ~/data/imagenet"
