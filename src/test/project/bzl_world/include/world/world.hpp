#pragma once

#include <boost/container/static_vector.hpp>

#include <string>

std::string getWorld();

inline std::size_t getSize()
{
    boost::container::static_vector<int, 10> numbers{2, 1, 2};
    return numbers.size();
}
