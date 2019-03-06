#include <iostream>
using namespace std;

int main(){

cout << endl << endl;
cout << "\033[7;36mInstructions:\033[0m\n";
cout << "\n\t\033[1;32m*\033[0m Type \033[1;36mls\033[0m to list all the files available.";
cout << "\n\t\033[1;32m*\033[0m Use \033[1;36mnano/vim {filename}\033[0m to edit file.";
cout << "\n\t\tEg. \033[1;36mnano main.cpp\033[0m";
cout << "\n\t\t  \033[1;36mctrl + x\033[0m to write changes made in the file.\n\t\t  Press \033[1;36my\033[0m to save the file.";
cout << "\n\t\033[1;32m*\033[0m Compile it manually: \'\033[1;36mg++ main.cpp -o myprog\033[0m\'.";
cout << "\n\t\033[1;32m*\033[0m Execute: \'\033[1;36m./myprog\033[0m\'.\n\n";
cout << "\n\033[1;32m>> \033[0mCode from textarea is saved in \033[1m\033[1;30;47m main.cpp \033[0m\033[0m and compiled to \033[1m\033[1;30;47m myprog \033[0m\033[0m";
cout << "\n\033[1;32m>> \033[0mEdit the code in  terminal \033[1m\033[1;30;47m nano main.cpp \033[0m\033[0m";
cout << "\n\033[1;32m>> \033[0mRun the compiled program: \033[1m\033[1;30;47m ./myprog \033[0m\033[0m";
cout << "\n\033[1;32m>> \033[0mUse command \033[1m\033[1;30;47m howto \033[0m\033[0m to display these instructions again\n\n\n";
cout << "\033[1;37mEnjoy!";
cout << "\n-Abhishek\033[0m\n\n";
return 0;
}