#include <iostream>
#include <vector>

using namespace std;

vector<int> test_vector = {
    // begin sourcegen test_vector
    3, 5, 21, 27, 30, 31, 32, 36, 45, 50, 54, 55, 58, 59, 60, 62, 63, 63, 67,
    69, 72, 73, 81, 89, 99
    // end sourcegen
};

int main() {
    for (auto& e : test_vector) { cout << e << endl; }
}
