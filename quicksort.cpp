#include <iostream>
#include <ctime>
using namespace std;
void partition(int *arr, int left ,int right) // thuật toán phân hoạch
{
	if (left >= right) return;

	int pivot = arr[(left + right) / 2];
	int i = left, j = right;

	while (i <= j)
	{
		while (arr[i] < pivot) i++;
		while (arr[j] > pivot) j--;
		if (i <= j)
		{
			swap(arr[i], arr[j]);
			i++;
			j--;
		}
	}

	partition(arr, left, j);
	partition(arr, i, right);

	return;
}
void quicksoft(int *arr, int n, int left, int right) // xuất thuật toán Quick Soft
{
	partition(arr, left, right);
	output(arr, n);
}
int main()
{
  int *arr, n;
  cout << "Input n : ";
  cin >> n;
  arr = new int[n];
  srand(time(0));
  for (int i = 0; i < n; i++)
  {
    arr[i] = rand()%200 + 30;
  }
  for (int i = 0; i < n; i++)
  {
    cout << arr[i] << "  ";
  }
  cout << endl;

}
