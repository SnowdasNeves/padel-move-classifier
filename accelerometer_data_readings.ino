// button A - changes between movement types
// button B - starts aquisition at 20 Hz of accelerometers

#include <M5StickCPlus.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>


// See the following for generating UUIDs version 4:
// https://www.uuidgenerator.net/
//this is what identifies your M5Stick. Must be personalized
#define DEVICE_NAME         "m5-tracer"
#define SERVICE_UUID        "175b68f3-9a62-4816-a08f-83ca36db642c"
#define CHARACTERISTIC_UUID "175b68f3-9a62-4816-a08f-83ca36db642c"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;


//Globals Variables
float accX = 0.0F;
float accY = 0.0F;
float accZ = 0.0F;

// float gyroX = 0.0F;
// float gyroY = 0.0F;
// float gyroZ = 0.0F;

bool acq_flag = false;
long acq_time = millis();
long acq_start_time;

//Callback on connection
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      M5.Lcd.println("BLE connect");
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      M5.Lcd.println("BLE disconnect");
      deviceConnected = false;
    }
};

//Callback to read and write messages
class MyCallbacks: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic *pCharacteristic) {
    M5.Lcd.println("Tx to RPI");
    pCharacteristic->setValue("Message from M5Stick");
  }
  
  void onWrite(BLECharacteristic *pCharacteristic) {
    M5.Lcd.println("Rx from RPI");
    std::string value = pCharacteristic->getValue();
    M5.Lcd.println(value.c_str()); // check if this appears on the Lcd when writting in the RPI
  }
};

//setups the necessary hardware
void setup() {
  Serial.begin(115200);
  M5.begin();
  M5.Lcd.println("BLE start.");

  BLEDevice::init(DEVICE_NAME);
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_INDICATE
                                       );
  pCharacteristic->setCallbacks(new MyCallbacks());
  pCharacteristic->addDescriptor(new BLE2902());

  pService->start();
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
  M5.Lcd.println("BLE running.");

  M5.Lcd.println("IMU Starting...");
  M5.Imu.Init(); 
  M5.Lcd.println("IMU Ready.");
}

//Main Loop
void loop() {
  char buf[40];
      
  if (deviceConnected) {
    //If button B pressed, post BLE message and start/stop continuos aquisition
    if(M5.BtnB.wasPressed()) {
      acq_flag = true;
      acq_time=millis();
      acq_start_time=millis();
    }

    // aquisition at 40 samples a second for 2000 ms
    if(acq_flag == true) {
      if(millis() - acq_time >= 25) {
        M5.IMU.getAccelData(&accX, &accY, &accZ);
        // M5.IMU.getGyroData(&gyroX, &gyroY, &gyroZ);
        snprintf(buf, sizeof(buf), "%6.2f, %6.2f, %6.2f", accX, accY, accZ);
        pCharacteristic->setValue(buf);
        pCharacteristic->notify();
        acq_time=millis();
        if (millis() - acq_start_time > 2000) {
          acq_flag = false;
        }
      }
    }
  }
  M5.update();
}
