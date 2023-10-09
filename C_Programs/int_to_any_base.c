#include <stdio.h>
#include <unistd.h>
#include <string.h>

void ft_putnbr_base(int nbr, char *base)
{
    int base_size;
    int i;
    int x;
    char array[42];

    base_size = 0;
    while (base[base_size] != '\0')
    {
        base_size++;
    }
    if(nbr < 0)
	    {
            if(nbr == -2147483648)
            {
                write(1, &"-2147483648", 12);	
                return;
            }
            write(1, &"-", 1);
            nbr = nbr * (-1);
	    }

    i = 0;
    while (nbr > 0)
    {
    x = nbr % base_size;
    nbr = (nbr - x) / base_size;
    x = base[x];
    array[i] = x;
    i++;
    }  
    while (i >= '\0')
    {
        write(1, &array[i], 1);
        i--;
    }
    printf("\n");
}
//test
int main()
{
    char base[40] = "0123ABCPoVZ";
    ft_putnbr_base(42,base);
    return 0;
}
