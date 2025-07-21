def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_blog_page(client):
    response = client.get('/blog')
    assert response.status_code == 200 or response.status_code == 302  # If login required
