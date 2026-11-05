def test_index_page_serves_html(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sistema de Asistencia Escolar" in response.data
