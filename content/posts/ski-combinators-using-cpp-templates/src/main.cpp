using namespace std;

using a = void;
using b = void;

#define generic(T) template <typename T>

template <char Ch, typename... Args> struct Var {
  generic(X) using apply = Var<Ch, Args..., X>;
};

struct K2 {
  template <typename X> struct K1 {
    generic(Y) using apply = X;
  };

  generic(X) using apply = K1<X>;
};

using K = K2;

struct S3 {
  template <typename X> struct S2 {
    template <typename X, typename Y> struct S1 {
      generic(Z) using apply = X::apply<Z>::apply<Y::apply<Z>>;
    };

    generic(Y) using apply = S1<X, Y>;
  };

  generic(X) using apply = S2<X>;
};

using S = S3;

struct I {
  generic(X) using apply = X;
};

int main() {
  using a = Var<'a'>;
  using b = Var<'b'>;

  using e1 = S::apply<I>::apply<I>::apply<a>; // a(a)
  using TermReversal = S::apply<K::apply<S>::apply<I>>::apply<K>; 
  using ba = TermReversal::apply<a>::apply<b>;

  return 0;
}
