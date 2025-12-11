import db

if __name__ == '__main__':
    test_id = '9c6f02c0-80a9-5f94-a452-d4947554c9e2'
    try:
        r = db.save_conversation(test_id, 'user', 'this is a test message', meta={})
        print('RESULT:', getattr(r, 'data', r))
    except Exception as e:
        print('FAILED:', e)
