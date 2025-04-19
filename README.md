# ReLife - 이미지 생성형 A.I와 이미지 처리를 활용한 인테리어 시뮬레이션 서비스 (Image Processing Server)

* 4인 팀 프로젝트로 진행.
* 2024.03.05. - 2024.06.02.
* 해당 프로젝트를 주제로 논문 작성 결과, 2024년 한국디지털콘텐츠학회 하계종합학술대회 대학생 논문경진대회 발표논문 중 동상 논문으로 선정 됨.
<br><br><br>

# 개요

* ReLife 프로젝트에서 Image Processing을 담당하는 Flask Server.
* opencv를 이용한 이미지 스티칭으로 파노라마 이미지 생성 후 배럴 왜곡을 적용하여 360도 VR뷰에 출력 하기 위한 이미지 생성 서버.
<br><br>

# Architecture

![IPF flow](https://github.com/user-attachments/assets/11ec137a-61eb-44d0-bf87-8dd423ce1b24)
<br><br>

# 사용기술

* ### Flask
  * Next.js의 route API로부터 들어온 요청을 처리하기 위해 사용.
  * 가벼우면서도 HTTP 요청/응답 처리에 필요한 기능을 충분히 지원하는 Python 웹 서버 프레임워크라 판단하여 선택.
 
* ### OpenCV
  * 사용자에게 받은 이미지를 이미지 스티칭을 활용하여 이어 붙인 파노라마 이미지로 만들기 위해 사용.
  * 사용자에게 제공되거나, 이미지 변환에 활용할 이미지에 각종 보정 효과를 진행하기 위해 사용.
<br><br>

# 주요 개발내역

* ### 파노라마 이미지 생성 구현 ([코드위치](https://github.com/yangsp31/Image_Processing_Server/blob/master/panorama.py))
  * 특징점 검출, 특징점 매칭, 호모그래피 추정, 이미지 왜곡 및 구형 매핑, 블랜딩 순서로 진행되는 이미지 스티칭 기술을 OpenCV에서 제공하는 cv2.Stitcher을 사용하여 진행함.
<br><br>
![IP Stitching](https://github.com/user-attachments/assets/dbb102f2-0bba-47d0-b3cc-6eeb4f6f0920)

* ### Image Stitching 예시

![image](https://github.com/user-attachments/assets/733bb40d-177b-4aed-92c2-0c2cb5d99ea4)

----

* ### 파노라마 이미지를 360도 VR 뷰 출력시 발생하는 핀쿠션(오목렌즈 효과) 왜곡 상쇄 구현 ([코드위치](https://github.com/yangsp31/Image_Processing_Server/blob/master/distortion.py))
  * 외부 API를 통해 이미지 변환을 마친 파노라마 이미지를 360도 VR 뷰로 출력하기 위해, 투명한 구에 매핑하는 방식을 사용.
  * 사용자는 구의 내부에서 이미지를 바라보는 구조이기 때문에, 핀쿠션 왜곡(오목 렌즈 효과)이 발생하여 이미지가 비정상적으로 뒤틀리는 문제 발생.
  * 이미지에 극좌표(r, θ)를 활용한 비선형 함수 기반의 거리 조절 기법을 적용한 배럴 왜곡(볼록 렌즈 효과) 적용.
  * 완벽하게는 아니여도 유의미 하게 핀쿠션 왜곡(오목 렌즈 효과)을 상쇄할 수 있었음.
 
* 배럴왜곡 적용 예시
  * 왜곡 전

  ![image](https://github.com/user-attachments/assets/a56b618c-c85b-4555-a069-96bdc73f9853)

  * 왜곡 후

  ![image](https://github.com/user-attachments/assets/728c1602-11b7-4387-a817-62b147d6fa59)

  <br><br>

# 회고 & 개선 필요사항 (회고 원문 : [Velog](https://velog.io/@yang_seongp31/ReLife-Image-Processing-Server-Flask))

* ### Image Stitching
  * Image Stitching 진행 후, 결과 이미지는 왜곡되어 붙여졌기 때문에 이미지의 가장자리 영역에 불균형한 빈 공간을 의미하는 검은색으로 나타남.
  * 검은색을 없애기 위해 RGB가 검은색에서 다른 색으로 넘어가는 경계를 기준으로 이미지만 남도록 잘라보는 등의 시도를 함.
  * 하지만, 잘라내면 원하는 영역 만큼 잘라내지 못하고, 잘라내어도 이미지만 정확히 남도록 하지 못함.
  * 생각해보면, 360도 VR뷰로 출력하면 이미지가 존재하는 영역을 제외하고 모두 검은색으로 출력 되기 때문에 검은 영역을 잘라 낸다 하여도 크게 의미 없는 작업.
  * 검은 영역을 출력하지 않고 360도 VR뷰에 출력하려면 결론적으로 투명한 구를 모두 감쌀만큼의 크기를 가진 이미지여야 함.
  * 이미지를 그정도로 늘리면 비율도 깨지고 화질도 낮아지므로, 사실상 검은 영역을 제거하는것 보다는 비율과 화질을 유지한 채로 이미지를 늘리는 방법을 고려 했어야 함이 맞음.
  * 결론적으로, 보간법을 활용하여 최대한 이미지를 비율과 화질을 유지하며 늘리는 방법을 시도 하였다면 좋았을 것이라 판단.
<br><br>

* ### 개선사항
  * Image Stitching 후 발생하는 빈 공간을 보간법을 활용해, 원본 이미지의 비율과 화질을 최대한 유지하며 줄이는 방식으로 구축.




