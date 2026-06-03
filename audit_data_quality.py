import json, re

COMMON_WORDS = {
    'nationality', 'reason', 'because', 'about', 'would', 'could', 'should',
    'there', 'their', 'which', 'every', 'other', 'after', 'first', 'second',
    'number', 'different', 'important', 'mobile', 'people', 'between', 'children',
    'building', 'following', 'complete', 'question', 'section', 'example',
    'problem', 'address', 'current', 'recent', 'changes', 'involve',
    'magical', 'kingdom', 'develop', 'board', 'games', 'might', 'help',
    'populations', 'grown', 'visit', 'antique', 'apartments',
}

issues = []
total = 0
for book_id in [f'cam{i}' for i in range(14, 21)]:
    for dtype in ['reading', 'listening']:
        path = f'data/cambridge/{book_id}/{dtype}.json'
        try:
            with open(path) as f:
                data = json.load(f)
            for test in data.get('tests', []):
                for container in test.get('parts', test.get('passages', [])):
                    for q in container.get('questions', []):
                        total += 1
                        qid = q.get('id', '')
                        body = q.get('body', q.get('question', ''))
                        # Split words
                        splits = re.findall(r'\b([a-z]{2,})\s([a-z]{2,})\b', body, re.I)
                        for w1, w2 in splits:
                            combo = (w1 + w2).lower()
                            if combo in COMMON_WORDS:
                                issues.append(f'{qid} SPLIT: "{w1} {w2}" should be "{combo}" | {body[:100]}')
                        # Garbled chars
                        for char in ['^', '~', '`', '\x7f']:
                            if char in body:
                                issues.append(f'{qid} GARBLED: contains "{char}" | {body[:100]}')
                        # Pipe char used as separator in cam14
                        if '|' in body and book_id == 'cam14':
                            if '|' in body and len(body) < 150:
                                issues.append(f'{qid} PIPE: {body[:120]}')
        except Exception as e:
            issues.append(f'{book_id}/{dtype}: {e}')

print(f'Scanned {total} questions, found {len(issues)} issues:')
for i in issues[:40]:
    print(f'  {i}')
if len(issues) > 40:
    print(f'  ... and {len(issues) - 40} more')
