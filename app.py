from flask import Flask

app = Flask(__name__)

@app.route('/Flask/Generate', methods = ['POST'])
def Generate_Panoramic_Image() : 

    # 이곳을 기준으로 작업 진행 해 주시면 됩니다. 이곳에 모든 기능(코드)를 넣지 말고 추가로 파이썬 파일을 만들어서 import해서 사용하는 방식으로 하시면 됩니다.
     
    return 200

if __name__ == '__main__' : 
    app.run(host = '127.0.0.1', port = 5000, debug = True)