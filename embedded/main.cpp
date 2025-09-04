// imu 데이터 수집용 코드
#include <Arduino.h>
#include <Adafruit_MPU6050.h> // 주석표시는 다 추가 필요.
#include <Wire.h> //
#include <AsyncUDP.h>
#include <WiFi.h>
#include <string.h>

const char *ssid = ""; // 5G 연결하지말기
const char *password = ""; // 비번 없으면 비워두기

IPAddress remoteIP(192,168,0,13); //
const uint16_t remotePort = 1234; //

bool isConnect = false; // udp.connect() 성공 여부

AsyncUDP udp;

byte FSR_pin = 0, LED_pin = 1; // *꼭 바꾸기
byte PWM_max = 179, PWM_min = 90;

// ################

Adafruit_MPU6050 mpu; // IMU 
float x, y, z;

void setup(void)
{
  Serial.begin(115200);
  while(!Serial)
  {
    delay(10);
  }

  // 와이파이 연결
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    Serial.print(".");
  }
  Serial.println("\nWifi succeed");

  // UDP 연결
  if (udp.connect(remoteIP, remotePort)) // connect 하고 나면, udp.print()로 해당 주소에 데이터 보내기 가능.
  {
    Serial.println("UDP connect succeed");
    isConnect = true;
  } 
  else
  {
    Serial.println("UDP connect failed");
  }

  // IMU 센서 초기화
  while(!mpu.begin())
  {
    Serial.println("IMU sensor init failed");
    delay(100);
  }
  Serial.println("IMU sensor init succeed");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_1000_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_94_HZ);

}

bool isClick(int v){
  // 200 이상일 때만 유효
  return (v >= 200);
}

int fsr_to_pwm(int v)
{
  if (v >= 200 && v <= 800)
  {
    return(map(v, 200, 800, PWM_min, PWM_max)); // 200 ~ 800 -> 127 ~ 255 -> (30%) 89.9 ~ 178.5
  }
  else if (v > 800)
  {
    return(PWM_max);
  }
  else
  {
    return 0;
  }
}

void loop()
{
  byte count = 0;
  int PWM_value = 0; // 안눌렸을 때 LED 0 출력.
  int FSR_value = analogRead(FSR_pin);
  sensors_event_t a, g, temp;

  // 눌렸을 때만 실행.
  if(isClick(FSR_value)) 
  {
    // LED 출력
    PWM_value = fsr_to_pwm(FSR_value);
    analogWrite(LED_pin, PWM_value);

    while(isClick(FSR_value) && count <= 80)
    {
      // 눌려있는 동안 값 보내기 (*모델 적용하고나서는 녹화방식으로 변경하기)
      mpu.getEvent(&a, &g, &temp);

      udp.printf("%.2f, %.2f, %.2f, %.2f, %.2f, %.2f", 
        a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z);
      
      count++;
      delay(20); // 50Hz
    }
    udp.print(count);
  }
  
  analogWrite(LED_pin, 0);

  Serial.print("sending data cnt = ");
  Serial.println(count);

  delay(500);
}
