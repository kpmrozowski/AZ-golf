#ifndef UTIL_IRANDOMGENERATOR_H
#define UTIL_IRANDOMGENERATOR_H

namespace golf::util {

class IRandomGenerator {
 public:
   [[nodiscard]] virtual double next_double(double max) noexcept = 0;
   [[nodiscard]] virtual int next_int(int max) noexcept = 0;
};

}

#endif//UTIL_IRANDOMGENERATOR_H
