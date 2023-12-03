import streamlit as st
from sqlalchemy import text

list_kelas = ['', 'Ekonomi', 'Bisnis', 'Eksekutif']
list_gender = ['', 'male', 'female']
lis_pelayanan_lainnya = ['', 'Makanan', 'Selimut', 'Bantal','Taksi', 'Asuransi']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://nisrina1802:FA6LmqkOR3KS@ep-fancy-thunder-58673639.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS STATION (id serial, nama text, gender text, \
                                                       tanggal_keberangkatan date, asal_stasiun text, tujuan_stasiun text, kelas text, nomor_kursi integer, pelayanan_lainnya text);')
    session.execute(query)'postgresql://nisrina1802:FA6LmqkOR3KS@ep-fancy-thunder-58673639.us-east-2.aws.neon.tech/web

st.header('GUBENG STATION DATA MANAGEMENT SYSTEM')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM station ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO station (nama, gender, tanggal_keberangkatan, asal_stasiun, tujuan_stasiun, kelas, nomor_kursi, pelayanan_lainnya) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':None, '4':'', '5':'', '6':'', '7':'', '8':'[]'})
            session.commit()

    data = conn.query('SELECT * FROM station ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_lama = result["nama"]
        gender_lama = result["gender"]
        tanggal_keberangkatan_lama = result["tanggal_keberangkatan"]
        asal_stasiun_lama = result["asal_stasiun"]
        tujuan_stasiun_lama = result["tujuan_stasiun"]
        kelas_lama = result["kelas"]
        nomor_kursi_lama = result["nomor_kursi"]
        pelayanan_lainnya_lama = result["pelayanan_lainnya"]

        with st.expander(f'a.n. {nama_lama}'):
            with st.form(f'data-{id}'):
                nama_baru = st.text_input("nama", nama_lama)
                gender_baru = st.selectbox("gender_name", list_gender, list_gender.index(gender_lama))
                tanggal_keberangkatan_baru = st.date_input("tanggal_keberangkatan", tanggal_keberangkatan_lama)
                asal_stasiun_baru = st.text_input("asal_stasiun", asal_stasiun_lama)
                tujuan_stasiun_baru = st.text_input("tujuan_stasiun", tujuan_stasiun_lama)
                kelas_baru = st.text_input("kelas", kelas_lama)
                nomor_kursi_baru = st.text_input("nomor_kursi", nomor_kursi_lama)
                pelayanan_lainnya_baru = st.multiselect("pelayanan_lainnya", ['Makanan', 'Selimut', 'Bantal','Taksi', 'Asuransi'], eval(pelayanan_lainnya_lama))
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE schedule \
                                          SET nama=:1, gender=:2, tanggal_keberangkatan=:3, asal_stasiun=:4, \
                                          tujuan_stasiun=:5, kelas=:6, nomor_kursi=:7, pelayanan_lainnya=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':nama_baru, '2':gender_baru, '3':tanggal_keberangkatan_baru, '4':asal_stasiun_baru, 
                                                    '5':tujuan_stasiun_baru, '6':kelas_baru, '7':nomor_kursi_baru, '8':str(pelayanan_lainnya_baru), '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM station WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
