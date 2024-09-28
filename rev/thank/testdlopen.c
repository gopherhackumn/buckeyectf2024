#include <dlfcn.h>
#include <stdio.h>

int main() {
	int result = (int) dlopen("./thing.o", RTLD_LAZY);
	printf("result %d\n", result);
}
