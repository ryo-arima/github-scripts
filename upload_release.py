import requests
import os

# GitHubの個人アクセストークン
GITHUB_TOKEN = 'your_personal_access_token'

# リポジトリの情報
REPO_OWNER = 'your_github_username_or_org'
REPO_NAME = 'your_repository_name'
RELEASE_TAG = 'v1.0.0'  # アップロードするリリースのタグ
RELEASE_NAME = 'Release v1.0.0'  # リリース名
RELEASE_BODY = 'Description of the release'  # リリースの説明

# アップロードするファイルのパス
FILE_PATH = 'path/to/your/file.zip'
FILE_NAME = os.path.basename(FILE_PATH)

# GitHub APIのエンドポイント
GITHUB_API_URL = 'https://api.github.com'

# リリースを作成する関数
def create_release():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    payload = {
        'tag_name': RELEASE_TAG,
        'name': RELEASE_NAME,
        'body': RELEASE_BODY,
        'draft': False,  # ドラフトを公開するかどうか
        'prerelease': False  # プレリリースにするかどうか
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print('Release created successfully.')
        return response.json()
    else:
        print(f"Failed to create release: {response.status_code} {response.text}")
        return None

# アセットをアップロードする関数
def upload_asset(upload_url):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/zip'  # アップロードするファイルのMIMEタイプを指定
    }
    params = {
        'name': FILE_NAME
    }
    
    with open(FILE_PATH, 'rb') as file:
        response = requests.post(upload_url, headers=headers, params=params, data=file)
        
        if response.status_code == 201:
            print('Asset uploaded successfully.')
        else:
            print(f"Failed to upload asset: {response.status_code} {response.text}")

# メイン処理
def main():
    release = create_release()
    
    if release:
        upload_url = release['upload_url'].split('{')[0]  # アップロードURLの取得
        upload_asset(upload_url)

if __name__ == "__main__":
    main()