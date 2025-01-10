Bu program, bir kamera ile canlı görüntü akışı alarak, belirli renklerdeki nesneleri tespit eder ve bu nesneleri takip eder. Kullanıcı, renkler, nesne boyutu ve mesafe hesaplamaları için ayarları yapabilmek için bir trackbar (kaydırıcı) arayüzü kullanabilir. Nesneler, kameradan uzaklıklarına ve renklerine göre sınıflandırılır ve ekranda görüntülenir.

Özellikler
Canlı video akışında renk tabanlı nesne tespiti
Nesne boyutuna ve mesafesine göre filtreleme
Nesne renk sınıflandırması (Kırmızı, Yeşil, Mavi)
Nesne takip sistemi (centrik izleme)
Kullanıcı dostu ayar penceresi ile nesne tespiti parametrelerinin ayarlanabilmesi
Başlangıç
Gereksinimler
Bu programın çalışması için aşağıdaki yazılımların yüklü olması gerekmektedir:

Python 3.x (Tercihen Python 3.7 ve üzeri)
OpenCV: Görüntü işleme ve nesne tespiti için kullanılır.
NumPy: Sayısal işlemler için gereklidir.
Kurulum Adımları
Python Yükleme: Python 3.x'i resmi Python web sitesinden indirebilirsiniz.

Gerekli Kütüphanelerin Yüklenmesi: Programın çalışabilmesi için OpenCV ve NumPy kütüphanelerine ihtiyacınız olacak. Aşağıdaki komutları kullanarak bu kütüphaneleri yükleyebilirsiniz:

pip install opencv-python
pip install numpy
Programı İndirme ve Çalıştırma: Programı bilgisayarınıza indirdikten sonra, Python dosyasını çalıştırabilirsiniz.

python main.py
Kullanım
Ana Pencereler
Object Detection:

Bu pencere, kameradan alınan görüntüdeki tespit edilen nesneleri gösterir.
Her nesne, etrafına bir bounding box (sınır kutusu) yerleştirilerek etiketlenir.
Nesnenin mesafesi ve renk adı ekranda görüntülenir.
Masks:

Bu pencere, nesne tespitine yönelik kullanılan maskeyi ve filtreleri gösterir.
Program, her renk için bir maske oluşturur ve bu maskenin üzerinden nesneleri tespit eder.
Settings:

Bu pencere, nesne tespiti parametrelerini ayarlamak için kullanılır.
Renk aralıkları (HSV değerleri), nesne genişliği, odak uzunluğu, minimum ve maksimum alan gibi parametreler bu pencere üzerinden ayarlanabilir.
Kontroller
Trackbars (Kaydırıcılar):

Renk aralıkları, nesne genişliği, odak uzunluğu gibi parametreleri değiştirmek için kullanılır.
Renk aralıkları: Kırmızı, yeşil ve mavi renkler için HSV (Hue, Saturation, Value) değerlerini ayarlayabilirsiniz.
Nesne Genişliği (cm): Kameradan tespit edilen nesnenin fiziksel genişliğini ayarlamak için kullanılır (cm cinsinden).
Odak Uzunluğu: Kameranın odak uzunluğunu ayarlamak için kullanılır.
Minimum/Maksimum Alan: Nesnelerin algılanması için minimum ve maksimum alan değerlerini belirler.
Ekran Üzerinde Bilgiler:

Tespit edilen nesnelerin mesafesi (cm cinsinden) ve rengi ekranda gösterilir.
Nesnenin etrafında bir bounding box (sınır kutusu) çizilir.
Çıkış
q tuşuna basarak programdan çıkabilirsiniz.
Özelleştirme
1. Renk Filtreleri:
Kırmızı, yeşil ve mavi renkler için HSV değerlerini Settings penceresindeki kaydırıcılar ile değiştirebilirsiniz. Renkler algılandığında, sistem bu renkleri tanır ve nesneleri sınıflandırır.
2. Nesne Takibi:
Nesneler, bulundukları yerden hareket ettikçe, program bu nesneleri takip eder. Takip, nesnenin centroid (merkez) noktası kullanılarak yapılır.
Nesne hareketleri belirli bir eşiği aşarsa, takip edilen nesne kaybolur ve yeni bir nesne olarak tanımlanır.
3. Mesafe Hesaplama:
Nesnelerin kameradan olan mesafesi, kullanılan odak uzunluğu ve nesne genişliği ile hesaplanır. Bu, nesnelerin fiziksel uzaklıklarını bilmenize olanak tanır.
