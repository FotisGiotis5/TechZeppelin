# 🚀 TechZeppelin

---

## "Shop Hard, Rock Harder — The Best Eshop in This Dimension"! 👋

# 🛒 Τι είναι

Η TechZeppelin είναι μια απλή αλλά λειτουργική εφαρμογή ηλεκτρονικού καταστήματος φτιαγμένη με Django. Οι χρήστες μπορούν να περιηγηθούν σε προϊόντα, να τα προσθέσουν στο καλάθι τους, να προχωρήσουν σε ολοκλήρωση αγοράς και να δουν το ιστορικό παραγγελιών τους.

## 🚀 Λειτουργίες

- Εγγραφή και σύνδεση χρήστη (authentication)
- Προβολή προϊόντων
- Προσθήκη προϊόντων στο καλάθι
- Ολοκλήρωση παραγγελίας (checkout)
- Καταγραφή και αποθήκευση ιστορικού παραγγελιών
- Προστασία προβολών με login

## 📦 Τεχνολογίες

- Python 3.13
- Django 5.1
- SQLite (προεπιλογή βάσης δεδομένων)
- HTML/CSS (για templates)

## 🔧 Εγκατάσταση

1. Κλωνοποίησε το αποθετήριο

git clone https://github.com/FotisGiotis5/TechZeppelin.git

2. Δημιούργησε και ενεργοποίησε ένα virtual environment

python -m venv venv

venv\Scripts\activate   # Για Windows

3. Εγκατάσταση των εξαρτήσεων

pip install -r requirements.txt

4. Εκτέλεσε τις μεταναστεύσεις της βάσης δεδομένων

python manage.py migrate

5. Εκκίνηση του development server

python manage.py runserver

6. Πρόσβαση στην εφαρμογή
   
Άνοιξε τον browser σου και πήγαινε στη διεύθυνση: http://localhost:8000
