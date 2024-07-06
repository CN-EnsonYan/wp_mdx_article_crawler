import requests
from bs4 import BeautifulSoup

# Crawl article data from the following site
def fetch_articles():
    url = 'https://blog.example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_tag = soup.find('main', {'class': 'postList mdui-center', 'id': 'postlist'})
    articles = main_tag.find_all('div', {'class': 'mdui-card postDiv mdui-center mdui-hoverable post-item'})

    article_data = []
    for i in range(2, 5):
        article = articles[i]
        cover_image_tag = article.find('div', {'class': 'post_list_t_img'})
        cover_image_url = cover_image_tag['data-bg']

        title_tag = article.find('div', {'class': 'mdui-card-primary-title'})
        title = title_tag.text.strip()

        description_tag = article.find('div', {'class': 'mdui-card-primary-subtitle'})
        description = description_tag.text.strip()

        # Get article link
        article_link = article.find('a')['href']

        # Get Date
        date_tag = article.find('span', {'class': 'info'}).find('i', {'class': 'mdui-icon'})
        date = date_tag.nextSibling.strip() if date_tag else ''

        article_data.append({
            'cover_image_url': cover_image_url,
            'title': title,
            'description': description,
            'article_link': article_link,
            'date': date
        })

    return article_data

# Generate Result HTML
# Feel free to modify it based on your final needs. Here is what I wrote for my personal homepage.
def generate_html(article_data):
    html_content = ''
    for article in article_data:
        html_content += f'''
        <div class="col-md-6 col-sm-6">
            <div class="custom-card">
                <div class="card-media">
                    <a href="{article['article_link']}" target="_blank">
                        <div class="card-image" style="background-image: url('{article['cover_image_url']}');" title="{article['title']}"></div>
                        <div class="card-overlay">
                            <div class="card-title">{article['title']}</div>
                            <div class="card-subtitle">{article['description']}</div>
                        </div>
                    </a>
                </div>
                <div class="card-actions">
                    <span class="info">
                        <i class="fa fa-clock-o"></i> {article['date']}
                    </span>
                    <a class="details-button" href="{article['article_link']}" target="_blank"><? echo $lang_sect_myblog_para_btn_template1; ?> &gt;</a>
                </div>
            </div>
        </div>\n'''
    return html_content

# Save HTML to File
def save_html(html_content):
    output_file_path = './articles.php'
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Execution: Crawling and Generating HTML
article_data = fetch_articles()
html_content = generate_html(article_data)
save_html(html_content)
print("HTML content has been saved to articles.html")
