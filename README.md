# moirai: MOre InstRuctions and Information

Backcronym. Anyway, this is a small project to extract useful instruction definitions
from LLVM's platform definitions. Projects like [capstone](https://github.com/capstone-project)
are amazing at what they do, but they aren't particularly useful for building analysis
tools because they don't preserve any information in a human-accessible format. THis aims
to borrow some of the techniques that `capstone` uses (using tblgen!) to quickly and
accurately build lots of instruction information.

