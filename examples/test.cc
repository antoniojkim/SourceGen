#include <iostream>
#include <vector>

using namespace std;

vector<int> test_vector = {
    // begin sourcegen test_vector
    10, 13, 17, 35, 41, 42, 70, 77, 84, 86
    // end sourcegen
};

int main() {
    for (auto& e : test_vector) { cout << e << endl; }
}
