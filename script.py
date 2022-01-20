from flask import Flask, request, make_response
import json
import pytils
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta


app = Flask(__name__)


def list_to_low(list_):
    return [x.lower() for x in list_]


def get_dict(city_line):
    city = city_line.split('\t')
    city_info = {
        'geonameid': city[0],
        'name': city[1],
        'asciiname': city[2],
        'alternatenames': city[3],
        'latitude': city[4],
        'longitude': city[5],
        'feature class': city[6],
        'feature code': city[7],
        'country code': city[8],
        'cc2': city[8],
        'admin1 code': city[9],
        'admin2 code': city[10],
        'admin3 code': city[11],
        'admin4 code': city[12],
        'population': city[13],
        'elevation': city[14],
        'dem': city[15],
        'timezone': city[16],
        'modification date': city[17]
    }
    return city_info


def time_difference(timeZone1, timeZone2):
    utcnow = timezone('utc').localize(datetime.utcnow())
    here = utcnow.astimezone(timezone(timeZone1)).replace(tzinfo=None)
    there = utcnow.astimezone(timezone(timeZone2)).replace(tzinfo=None)
    offset = relativedelta(here, there)
    return offset.hours


@app.route('/api/method1/<geonameid>')
def show_city_info(geonameid):
    if geonameid.isnumeric() is True:
        file = open('RU/RU.txt', 'r', encoding="utf-8")
        response = ''
        for line in file:
            if line.split('\t')[0] == geonameid:
                response = json.dumps(get_dict(line),
                                      ensure_ascii=False).encode('utf8')
                file.close()
                return make_response(response, 200)

        response = json.dumps("Not Found", ensure_ascii=False).encode('utf8')
        return make_response(response, 404)
    else:
        response = json.dumps("Not Found", ensure_ascii=False).encode('utf8')
        return make_response(response, 404)


@app.route('/api/method2')
def show_pages():
    page = request.args.get('page', default=1, type=int)
    num = request.args.get('num', default=1, type=int)

    response = {'page': '', 'number_of_cities': '', 'data': ''}
    response['page'] = page
    response['number_of_cities'] = num

    start = (page - 1)*num
    data = []

    file = open('RU/RU.txt', 'r', encoding="utf-8")
    cities = file.readlines()
    for i in range(start, start + num):
        try:
            data.append(get_dict(cities[i]))
        except Exception:
            response = json.dumps("Not Found",
                                  ensure_ascii=False).encode('utf8')
            make_response(response, 404)
    response['data'] = data
    return make_response(json.dumps(response,
                         ensure_ascii=False).encode('utf8'), 200)


@app.route('/api/method3/<names>')
def show_difference(names):
    names = names.split('&')
    response = {
        'city1': '',
        'city2': '',
        'additionally': {
            'closer to the north': '',
            'equality of time zones': '',
            'between': ''
            }
    }
    if len(names) == 2:
        file = open('RU/RU.txt', 'r', encoding="utf-8")

        city1 = ''
        city2 = ''
        population1 = -1
        population2 = -1

        for line in file:
            split_line = line.split('\t')

            all_names = []
            all_names.append(split_line[1])
            all_names.append(split_line[2])
            all_names.append(split_line[3])
            all_names = list_to_low(all_names)

            if split_line[13] == '':
                split_line[13] = 0

            if (names[0] in split_line or pytils.translit.slugify(names[0]) in all_names):
                if int(float(split_line[13])) > population1:
                    city1 = line
                    population1 = split_line[13]

            if (names[1] in split_line or pytils.translit.slugify(names[1]) in all_names):
                if int(float(split_line[13])) > population2:
                    city2 = line
                    population2 = split_line[13]

            #   Изначальный вариант, работает быстрее, возможно метод translit.slugify() замедляет перебор файла
            #   if ((names[0] in split_line[3]) and (int(float(split_line[13])) >= population1)):
            #       city1 = line
            #       population1 = split_line[13]
            #   if ((names[1] in split_line[3]) and (int(float(split_line[13])) >= population2)):
            #       city2 = line
            #       population2 = split_line[13]

        if (city1 != '') and (city2 != ''):
            response['city1'] = get_dict(city1)
            response['city2'] = get_dict(city2)

            if response['city1']['longitude'] > response['city2']['longitude']:
                response['additionally']['closer to the north'] = response['city1']['name']

            elif response['city1']['longitude'] < response['city2']['longitude']:
                response['additionally']['closer to the north'] = response['city2']['name']

            else:
                response['additionally']['closer to the north'] = "identically"

            if response['city1']['timezone'] == response['city2']['timezone']:
                response['additionally']['equality of time zones'] = True
            else:
                response['additionally']['equality of time zones'] = False

            response['additionally']['between'] = time_difference(
                response['city1']['modification date'],
                response['city2']['modification date'])

            response = json.dumps(response, ensure_ascii=False).encode('utf8')
            return make_response(response, 200)

        else:
            response = json.dumps("Not Found", ensure_ascii=False).encode('utf8')
            return make_response(response, 404)

    response = json.dumps("Bad Request", ensure_ascii=False).encode('utf8')
    return make_response(response, 400)


@app.route('/api/additional_method/<part_name>')
def filter(part_name):
    file = open('RU/RU.txt', 'r', encoding="utf-8")
    part_name = pytils.translit.slugify(part_name)
    result = []

    for line in file:
        split_line = line.split('\t')

        all_names = []
        all_names.append(split_line[1])
        all_names.append(split_line[2])
        all_names.append(split_line[3])
        all_names = list_to_low(all_names)

        for name in all_names:
            if part_name in name:
                result.append(split_line[1])

    if len(result) == 0:
        response = json.dumps("Not Found", ensure_ascii=False).encode('utf8')
        return make_response(response, 404)

    response = json.dumps(result, ensure_ascii=False).encode('utf8')
    return make_response(response, 200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
