#include <iostream>

// Note: Use 64bit integers everywhere

// Utility
static inline int cmp(long long int a, long long int b)
{
    // a < b: -1
    // a > b:  1
    // a = b:  0
    return ((a < b) - (a > b));
}

struct Vector3d {
    long long int x;
    long long int y;
    long long int z;
};

typedef Vector3d Velocity;
typedef Vector3d Position;

static std::ostream& operator << (std::ostream &o,const Vector3d &v) {
    o << "{" << v.x << "," << v.y << "," << v.z << "}";
    return o;
}

static inline Vector3d operator + (const Vector3d &a, const Vector3d &b) {
    long long int sx = a.x + b.x;
    long long int sy = a.y + b.y;
    long long int sz = a.z + b.z;
    Vector3d sum = {sx, sy, sz};
    return sum;
}

struct Moon {
    Position p0; // Save original position
    Position p;
    Velocity v;
};

static std::ostream& operator << (std::ostream &o, const Moon &m) {
    o << "p0=" << m.p0 << ", p=" << m.p << ", v=" << m.v;
    return o;
}

// Multiple input options
//Position p_start[4] = { {-1, 0, 2},
//                        {2, -10, -7},
//                        {4, -8, 8},
//                        {3, 5, -1} };

//Position p_start[4] = {{-8, -10, 0},
//                       {5, 5, 10},
//                       {2, -7, 3},
//                       {9, -8, -3} };

Position p_start[4] = { {3, 15, 8},
                        {5, -1, -2},
                        {-10, 8, 2},
                        {8, 4, -5} };

struct Moon moons[4] = { {p_start[0], p_start[0], {0, 0, 0}},
                         {p_start[1], p_start[1], {0, 0, 0}},
                         {p_start[2], p_start[2], {0, 0, 0}},
                         {p_start[3], p_start[3], {0, 0, 0}}};

// Debug
void show(void)
{
    std::cout << moons[0] << std::endl;
    std::cout << moons[1] << std::endl;
    std::cout << moons[2] << std::endl;
    std::cout << moons[3] << std::endl;

    std::cout << std::endl;
}

// Main simulation loop
bool step(void)
{

    // Update velocity, for all pairs
    // 0, 1
    long long int dx01 = cmp(moons[0].p.x, moons[1].p.x);
    long long int dy01 = cmp(moons[0].p.y, moons[1].p.y);
    long long int dz01 = cmp(moons[0].p.z, moons[1].p.z);

    // 0, 2
    long long int dx02 = cmp(moons[0].p.x, moons[2].p.x);
    long long int dy02 = cmp(moons[0].p.y, moons[2].p.y);
    long long int dz02 = cmp(moons[0].p.z, moons[2].p.z);

    // 0, 3
    long long int dx03 = cmp(moons[0].p.x, moons[3].p.x);
    long long int dy03 = cmp(moons[0].p.y, moons[3].p.y);
    long long int dz03 = cmp(moons[0].p.z, moons[3].p.z);

    // 1, 2
    long long int dx12 = cmp(moons[1].p.x, moons[2].p.x);
    long long int dy12 = cmp(moons[1].p.y, moons[2].p.y);
    long long int dz12 = cmp(moons[1].p.z, moons[2].p.z);

    // 1, 3
    long long int dx13 = cmp(moons[1].p.x, moons[3].p.x);
    long long int dy13 = cmp(moons[1].p.y, moons[3].p.y);
    long long int dz13 = cmp(moons[1].p.z, moons[3].p.z);

    // 2, 3
    long long int dx23 = cmp(moons[2].p.x, moons[3].p.x);
    long long int dy23 = cmp(moons[2].p.y, moons[3].p.y);
    long long int dz23 = cmp(moons[2].p.z, moons[3].p.z);

    moons[0].v.x += dx01 + dx02 + dx03;
    moons[0].v.y += dy01 + dy02 + dy03;
    moons[0].v.z += dz01 + dz02 + dz03;

    moons[1].v.x += -dx01 + dx12 + dx13;
    moons[1].v.y += -dy01 + dy12 + dy13;
    moons[1].v.z += -dz01 + dz12 + dz13;

    moons[2].v.x += -dx02 - dx12 + dx23;
    moons[2].v.y += -dy02 - dy12 + dy23;
    moons[2].v.z += -dz02 - dz12 + dz23;

    moons[3].v.x += -dx03 - dx13 - dx23;
    moons[3].v.y += -dy03 - dy13 - dy23;
    moons[3].v.z += -dz03 - dz13 - dz23;

    // Update position based on updated velocity
    moons[0].p = moons[0].p + moons[0].v;
    moons[1].p = moons[1].p + moons[1].v;
    moons[2].p = moons[2].p + moons[2].v;
    moons[3].p = moons[3].p + moons[3].v;

    bool cycle;
    int i = 2;
    if (moons[i].v.x == 0 && 
        moons[i].v.y == 0 && 
        moons[i].v.z == 0) {
        if (moons[i].p.x == moons[i].p0.x && 
            moons[i].p.y == moons[i].p0.y && 
            moons[i].p.z == moons[i].p0.z) {
            cycle = true;
        } else {
            cycle = false;
        }
    } else {
        cycle = false;
    }

    return cycle;
}

int main()
{
    bool done = false;
    long long int i = 0;
    while(!done) {
        //if (i%1000000 == 0)
        //    std::cout << (long long int)(i/1000000) << "M+" << std::endl;
        i += 1;
        done = step();
    }

    std::cout << i << ": " << std::endl;
    show();

    return 0;
}
