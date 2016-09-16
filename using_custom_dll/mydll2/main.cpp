
extern "C" __declspec(dllexport)
int add(int a, int b)
{
	return a + b;
}

extern "C" __declspec(dllexport) 
int sub(int a, int b)
{
	return a - b;
}
