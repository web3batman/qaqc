import pandas as pd
def all_files(service):
    result = []
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        
        result.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    return result

def items_folder(service, path):
    query = "title='{}'".format(path)
    f_id = service.files().list(q=query,pageToken=None).execute()['items'][0]['id']
    page_token = None
    while True:
        result = []
        param = {}
        if page_token:
            param['pageToken'] = page_token
        children = service.children().list(folderId=f_id, **param).execute()
        result.extend(children['items'])
        page_token = children.get('nextPageToken')
        if not page_token:
            break
    result = [service.files().get(fileId=x['id'] ).execute() for x in result]

    return result