#include <math.h>
#include <Servo.h>

Servo servo1, servo2;

const double L1 = 13.4, L2 = 16.4, L3 = 4.8;

double calculateRadian(double x, double y, bool isRight)
{
  double alpha = -(x + (isRight ? -L3 : L3)) / y;
  double beta = (pow(x, 2) + pow(y, 2) - pow(L3, 2) + pow(L1, 2) - pow(L2, 2)) / (2 * y);

  double A = 1 + pow(alpha, 2);
  double B = L3 + alpha * beta * (isRight ? -1 : 1);
  double C = pow(L3, 2) - pow(L1, 2) + pow(beta, 2);

  double X = (isRight ? 1 : -1) * (B + sqrt(pow(B, 2) - A * C)) / A;
  double Y = alpha * X + beta;

  return asin(Y / L1);
}

void servoWrite(double angle1, double angle2)
{
  const int k = 2300 - 700;

  int pw1 = angle1 / M_PI * k + 700;
  int pw2 = angle2 / M_PI * k + 700;

  servo1.writeMicroseconds(pw1);
  servo2.writeMicroseconds(pw2);
}

void point(double x, double y)
{
  servoWrite(calculateRadian(x, y, false), M_PI - calculateRadian(x, y, true));
}

void line()
{
  point(0.0, 5.0);
  delay(10000);

  for (int i = 0; i <= 150 + 60; i++)
  {
    double x = -5.0 / 150.0 * (i / 10.0);
    double y = 5.0 + (i / 10.0);

    point(x, y);
    delay(50);
  }
}

void circle()
{
  const double h1 = 10.0 / 10.2, h2 = 10.0 / 9.0;

  double x = 1;
  double y = L2 + 6;

  // point(x, y);
  // delay(5000);

  x = 1 + 5 * h1 * cos(0);
  y = L2 + 6 + 5 * h2 * sin(0);

  point(x, y);
  delay(10000);

  for (int i = 0; i <= (360 + 15) * 2; i++)
  {
    x = 1 + 5 * h1 * cos((i / 2.0) * (M_PI / 180.0));
    y = L2 + 6 + 5 * h2 * sin((i / 2.0) * (M_PI / 180.0));

    point(x, y);
    delay(30);
  }
}

void setup()
{
  Serial.begin(9600);
  delay(30);

  servo1.attach(10, 700, 2300);
  servo2.attach(11, 700, 2300);
  delay(30);

  // line();
  circle();
}

void loop()
{
}
