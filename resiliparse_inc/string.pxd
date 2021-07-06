# Complete redeclaration of libcpp.string, since Cython's std::string is vastly incomplete and buggy.

# Fixed std::string::npos (see: https://github.com/cython/cython/issues/4268_
cdef extern from "<string>" namespace "std::string" nogil:
    const size_t npos

# Copy of https://github.com/cython/cython/blob/master/Cython/Includes/libcpp/string.pxd with additions at the end
cdef extern from "<string>" namespace "std" nogil:
    cdef cppclass string:
        cppclass iterator:
            iterator()
            char& operator*()
            iterator(iterator &)
            iterator operator++()
            iterator operator--()
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass reverse_iterator:
            char& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator>=(reverse_iterator)
        cppclass const_iterator(iterator):
            pass
        cppclass const_reverse_iterator(reverse_iterator):
            pass

        string() except +
        string(const char *) except +
        string(const char *, size_t) except +
        string(const string&) except +
        # as a string formed by a repetition of character c, n times.
        string(size_t, char) except +
        # from a pair of iterators
        string(iterator first, iterator last) except +

        iterator begin()
        const_iterator const_begin "begin"()
        iterator end()
        const_iterator const_end "end"()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()

        const char* c_str()
        const char* data()
        size_t size()
        size_t max_size()
        size_t length()
        void resize(size_t)
        void resize(size_t, char c)
        size_t capacity()
        void reserve(size_t)
        void clear()
        bint empty()
        iterator erase(iterator position)
        iterator erase(const_iterator position)
        iterator erase(iterator first, iterator last)
        iterator erase(const_iterator first, const_iterator last)

        char& at(size_t) except +
        char& operator[](size_t)
        char& front()  # C++11
        char& back()   # C++11
        int compare(const string&)

        string& append(const string&) except +
        string& append(const string&, size_t, size_t) except +
        string& append(const char *) except +
        string& append(const char *, size_t) except +
        string& append(size_t, char) except +

        void push_back(char c) except +

        string& assign (const string&)
        string& assign (const string&, size_t, size_t)
        string& assign (const char *, size_t)
        string& assign (const char *)
        string& assign (size_t n, char c)

        string& insert(size_t, const string&) except +
        string& insert(size_t, const string&, size_t, size_t) except +
        string& insert(size_t, const char* s, size_t) except +


        string& insert(size_t, const char* s) except +
        string& insert(size_t, size_t, char c) except +

        size_t copy(char *, size_t, size_t) except +

        size_t find(const string&, size_t pos)
        size_t find(const string&)
        size_t find(const char*, size_t pos, size_t n)
        size_t find(const char*, size_t pos)
        size_t find(const char*)
        size_t find(char c, size_t pos)
        size_t find(char c)

        size_t rfind(const string&, size_t pos)
        size_t rfind(const string&)
        size_t rfind(const char* s, size_t pos, size_t n)
        size_t rfind(const char*, size_t pos)
        size_t rfind(const char*)
        size_t rfind(char c, size_t pos)
        size_t rfind(char c)

        size_t find_first_of(const string&, size_t pos)
        size_t find_first_of(const string&)
        size_t find_first_of(const char* s, size_t pos, size_t n)
        size_t find_first_of(const char*, size_t pos)
        size_t find_first_of(const char*)
        size_t find_first_of(char c, size_t pos)
        size_t find_first_of(char c)

        size_t find_first_not_of(const string&, size_t pos)
        size_t find_first_not_of(const string&)
        size_t find_first_not_of(const char* s, size_t, size_t)
        size_t find_first_not_of(const char*, size_t pos)
        size_t find_first_not_of(const char*)
        size_t find_first_not_of(char c, size_t pos)
        size_t find_first_not_of(char c)

        size_t find_last_of(const string&, size_t pos)
        size_t find_last_of(const string&)
        size_t find_last_of(const char* s, size_t pos, size_t n)
        size_t find_last_of(const char*, size_t pos)
        size_t find_last_of(const char*)
        size_t find_last_of(char c, size_t pos)
        size_t find_last_of(char c)

        size_t find_last_not_of(const string&, size_t pos)
        size_t find_last_not_of(const string&)
        size_t find_last_not_of(const char* s, size_t pos, size_t n)
        size_t find_last_not_of(const char*, size_t pos)
        size_t find_last_not_of(const char*)
        size_t find_last_not_of(char c, size_t pos)
        size_t find_last_not_of(char c)

        string substr(size_t, size_t) except +
        string substr()
        string substr(size_t) except +

        #string& operator= (const string&)
        #string& operator= (const char*)
        #string& operator= (char)

        string operator+ (const string& rhs) except +
        string operator+ (const char* rhs) except +

        bint operator==(const string&)
        bint operator==(const char*)

        bint operator!= (const string& rhs )
        bint operator!= (const char* )

        bint operator< (const string&)
        bint operator< (const char*)

        bint operator> (const string&)
        bint operator> (const char*)

        bint operator<= (const string&)
        bint operator<= (const char*)

        bint operator>= (const string&)
        bint operator>= (const char*)

        # ADDITIONS:
        string& erase(size_t index, size_t count)


    string to_string(int val)
    string to_string(long val)
    string to_string (long long val)
    string to_string (unsigned val)
    string to_string (unsigned long val)
    string to_string (unsigned long long val)
    string to_string (float val)
    string to_string (double val)
    string to_string (long double val)

    # ADDITIONS:
    string to_string(size_t i)