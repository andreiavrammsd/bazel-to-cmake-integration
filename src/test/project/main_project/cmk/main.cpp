#include <bzl.hpp>
#include <header.hpp>
#include <world/world.hpp>

#include <iostream>

int main()
{
    std::cout << "Hello, " << getWorld() << ", " << getHeader() << "," << getSize() << "," << getBzl() << std::endl;
    return 0;
}
