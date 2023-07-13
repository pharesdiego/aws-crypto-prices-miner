from bs4 import BeautifulSoup

def handler(event, context):
    html = event['html']
    soup = BeautifulSoup(html, features='html5lib')
    rows = soup.find_all('tr')

    tables_rows = [
        [el.text for el in els] for els in [row.find_all(['p', 'span']) for row in rows[1:]]
    ]

    first_10_rows = [','.join([r[2], r[3], r[4]]) for r in tables_rows[:10]]

    rest_rows = [','.join([r[3], r[4], r[5]]) for r in tables_rows[10:]]

    header = 'name,symbol,price\n'
    csv = header + '\n'.join(first_10_rows + rest_rows)

    return csv
