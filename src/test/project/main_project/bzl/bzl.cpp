#include "bzl.hpp"

#include <boost/container/static_vector.hpp>

#include <string>

std::string getBzl()
{
    boost::container::static_vector<int, 2> numbers{1, 2};
    return std::to_string(numbers.size());
}
