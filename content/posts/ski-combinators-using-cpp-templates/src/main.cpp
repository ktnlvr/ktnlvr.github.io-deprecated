#include <iostream>

using namespace std;

#define Var(ch)                                                                \
  template <typename... Args> struct _##ch {                                   \
    template <typename X> using apply = _##ch<Args..., X>;                     \
  };                                                                           \
  using ch = _##ch<>;

struct K2 {
  template <typename X> struct K1 {
    template <typename Y> using apply = X;
  };

  template <typename X> using apply = K1<X>;
};

using K = K2;

struct S3 {
  template <typename X, typename Y> struct S1 {
    template <typename Z> using helper = typename Y::apply<Z>;

    template <typename Z> using apply = typename X::apply<Z>::apply<helper<Z>>;
  };

  template <typename X> struct S2 {
    template <typename Y> using apply = S1<X, Y>;
  };

  template <typename X> using apply = S2<X>;
};

using S = S3;

struct I {
  template <typename X> using apply = X;
};

struct J {
  template <typename X> using apply = typename X::apply<S>::apply<K>;
};

// This is the omega combinator, since they get stuck in an infinite loop we
// can't even define them in a file without getting a compile error
#ifdef 0
struct ω {
  template <typename X> using apply = typename X::apply<X>;
};

using Ω = ω::apply<ω>;
#endif

Var(a);
Var(b);
Var(c);
int main() {
  using e1 = I; // a(a)
  using e2 = S::apply<K::apply<S::apply<I>>>::apply<K>;
  using e3 = e2::apply<a>::apply<b>;
  using e4 = a::apply<b>;
  using e5 = S::apply<K>::apply<K::apply<K>>;
  using e6 = e5::apply<a>;
  using e7 = J::apply<J>::apply<a>; // I expressed with Iota

  return 0;
}
