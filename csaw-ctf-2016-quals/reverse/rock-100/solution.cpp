#include <string>
#include <iostream>

using namespace std;

int main(){
	string solution = "FLAG23456912365453475897834567";
	for(int i =0; i <= solution.length();i++){
		solution[i] = char(((solution[i]-(265%999))^0x10));
	} 	

	for(int j =0; j <= solution.length();j++){
		solution[j] = char((solution[j] - 20)^0x50);
	
	}

	cout << "FLAG:" << solution << endl;



}
