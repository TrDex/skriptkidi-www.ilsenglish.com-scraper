#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple script for answer selection and scraping their text representation
from https://www.ilsenglish.com/quicklinks/test-your-english-level
∞
Created by Mykola Soloduha (mykola.soloduha@gmail,com),
TIT Inc.,
2019
"""

import json
import re

import requests
from bs4 import BeautifulSoup

test_page_url = 'https://www.ilsenglish.com/quicklinks/test-your-english-level'
ajax_url = 'https://www.ilsenglish.com/ajax/onlinetesting/'
method = 'POST'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}


def main():
    data = dict()
    data['type'] = 'onlinetesting'
    data['test'] = 1

    for n in range(1, 51):
        data[f'answers[question-{n}]'] = 1

    correct_answers = {}
    for n in range(1, 51):
        results = {}
        for key, item in correct_answers.items():
            data[f'answers[question-{key}]'] = item

        for i in range(1, 5):
            data[f'answers[question-{n}]'] = i

            request = requests.request(method, ajax_url, data=data, headers=headers)
            response = json.loads(request.text)
            response_text = response['data']
            result = int(re.search(r'([\d]{1,3})%!', response_text).group(1))
            results[i] = result

        best_result = max(results.values())
        for key, item in results.items():
            if item == best_result:
                correct_answers[n] = key
                # print(f'Correct answer for Q{n} is {key}')

    # Let's display text answers using the site containing the questions
    site_text = requests.get(test_page_url).text
    soup = BeautifulSoup(site_text, 'html.parser')

    inline_answers = []
    for key, item in correct_answers.items():
        attrs = {
            'name': f'question-{key}',
            'value': f'{item}'
        }
        html_input = soup.find('input', attrs=attrs)

        label = html_input.parent
        div = label.parent
        div.find('h2').find('span').replace_with(f'`{label.text}`')
        inline_answer = div.find('h2').text
        inline_answers.append(inline_answer)

    print('\n\n')
    print('Answers: \n')
    for inline_answer in inline_answers:
        print(inline_answer)


if __name__ == '__main__':
    print('The process has been started. It may take a few minutes...')
    main()
