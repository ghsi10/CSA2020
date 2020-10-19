#include <stdio.h>

typedef struct rc2_key_st {
    unsigned short xkey[64];
} RC2_Schedule;
typedef	struct
{
	unsigned char  key[16];
	unsigned char second_flag[24];
} gametype;

void rc2_keyschedule( RC2_Schedule *key_schedule,
                      const unsigned char *key,
                      unsigned len,
                      unsigned bits )
        {
        unsigned char x;
        unsigned i;
        /* 256-entry permutation table, probably derived somehow from pi */
        static const unsigned char permute[256] = {
            217,120,249,196, 25,221,181,237, 40,233,253,121, 74,160,216,157,
            198,126, 55,131, 43,118, 83,142, 98, 76,100,136, 68,139,251,162,
             23,154, 89,245,135,179, 79, 19, 97, 69,109,141,  9,129,125, 50,
            189,143, 64,235,134,183,123, 11,240,149, 33, 34, 92,107, 78,130,
             84,214,101,147,206, 96,178, 28,115, 86,192, 20,167,140,241,220,
             18,117,202, 31, 59,190,228,209, 66, 61,212, 48,163, 60,182, 38,
            111,191, 14,218, 70,105,  7, 87, 39,242, 29,155,188,148, 67,  3,
            248, 17,199,246,144,239, 62,231,  6,195,213, 47,200,102, 30,215,
              8,232,234,222,128, 82,238,247,132,170,114,172, 53, 77,106, 42,
            150, 26,210,113, 90, 21, 73,116, 75,159,208, 94,  4, 24,164,236,
            194,224, 65,110, 15, 81,203,204, 36,145,175, 80,161,244,112, 57,
            153,124, 58,133, 35,184,180,122,252,  2, 54, 91, 37, 85,151, 49,
             45, 93,250,152,227,138,146,174,  5,223, 41, 16,103,108,186,201,
            211,  0,230,207,225,158,168, 44, 99, 22,  1, 63, 88,226,137,169,
             13, 56, 52, 27,171, 51,255,176,187, 72, 12, 95,185,177,205, 46,
            197,243,219, 71,229,165,156,119, 10,166, 32,104,254,127,193,173
        };
        if (!bits)
                bits = 1024;
        memcpy(&key_schedule->xkey, key, len);
        /* Phase 1: Expand input key to 128 bytes */
        if (len < 128) {
                i = 0;
                x = ((unsigned char *)key_schedule->xkey)[len-1];
                do {
                        x = permute[(x + ((unsigned char *)key_schedule->xkey)[i++]) & 255];
                        ((unsigned char *)key_schedule->xkey)[len++] = x;
                } while (len < 128);
        }
        /* Phase 2 - reduce effective key size to "bits" */
        len = (bits+7) >> 3;
        i = 128-len;
        x = permute[((unsigned char *)key_schedule->xkey)[i] & (255 >> (7 & -bits))];
        ((unsigned char *)key_schedule->xkey)[i] = x;
        while (i--) {
                x = permute[ x ^ ((unsigned char *)key_schedule->xkey)[i+len] ];
                ((unsigned char *)key_schedule->xkey)[i] = x;
        }
        /* Phase 3 - copy to xkey in little-endian order */
        i = 63;
        do {
                key_schedule->xkey[i] =  ((unsigned char *)key_schedule->xkey)[2*i] +
                          (((unsigned char *)key_schedule->xkey)[2*i+1] << 8);
        } while (i--);
        }

void rc2_decrypt( const RC2_Schedule *key_schedule,
                  unsigned char *plain,
                  const unsigned char *cipher )
        {
        unsigned x76, x54, x32, x10, i;
        x76 = (cipher[7] << 8) + cipher[6];
        x54 = (cipher[5] << 8) + cipher[4];
        x32 = (cipher[3] << 8) + cipher[2];
        x10 = (cipher[1] << 8) + cipher[0];
        i = 15;
        do {
                x76 &= 65535;
                x76 = (x76 << 11) + (x76 >> 5);
                x76 -= (x10 & ~x54) + (x32 & x54) + key_schedule->xkey[4*i+3];
                x54 &= 65535;
                x54 = (x54 << 13) + (x54 >> 3);
                x54 -= (x76 & ~x32) + (x10 & x32) + key_schedule->xkey[4*i+2];
                x32 &= 65535;
                x32 = (x32 << 14) + (x32 >> 2);
                x32 -= (x54 & ~x10) + (x76 & x10) + key_schedule->xkey[4*i+1];
                x10 &= 65535;
                x10 = (x10 << 15) + (x10 >> 1);
                x10 -= (x32 & ~x76) + (x54 & x76) + key_schedule->xkey[4*i+0];
                if (i == 5 || i == 11) {
                        x76 -= key_schedule->xkey[x54 & 63];
                        x54 -= key_schedule->xkey[x32 & 63];
                        x32 -= key_schedule->xkey[x10 & 63];
                        x10 -= key_schedule->xkey[x76 & 63];
                }
        } while (i--);
        plain[0] = (unsigned char)x10;
        plain[1] = (unsigned char)(x10 >> 8);
        plain[2] = (unsigned char)x32;
        plain[3] = (unsigned char)(x32 >> 8);
        plain[4] = (unsigned char)x54;
        plain[5] = (unsigned char)(x54 >> 8);
        plain[6] = (unsigned char)x76;
        plain[7] = (unsigned char)(x76 >> 8);
        }



int rc2_cc_set_key(
	RC2_Schedule *cx,
	const void *rawKey,
	size_t keyLength)
{

	rc2_keyschedule(cx, rawKey, keyLength, keyLength*8);
	return 0;
}

void rc2_cc_decrypt(RC2_Schedule *cx, const void *blockIn, void *blockOut)
{
	rc2_decrypt(cx, (unsigned char *)blockOut, (const unsigned char *)blockIn);
}


int main() {
    gametype gamestate;
    RC2_Schedule cx;
    unsigned char res[64];
    unsigned char arr2[24] = {0x61, 0x71, 0xf9, 0x53, 0xa6, 0x63, 0x65, 0x2, 0xc7, 0x15, 0xf0, 0x70, 0xf1, 0x95, 0x66,
                              0x1, 0x6, 0x50, 0x17, 0x35, 0x1c, 0x12, 0xc0, 0xfb};
    gamestate.key[0]=109;
    gamestate.key[1]=168;
    gamestate.key[2]=20;
    gamestate.key[3]=145;
    gamestate.key[4]=61;
    gamestate.key[5]=98;
    gamestate.key[6]=61;
    gamestate.key[7]=98;
    gamestate.key[8]=227;
    gamestate.key[9]=156;
    gamestate.key[10]=156;
    gamestate.key[11]=198;
    gamestate.key[12]=198;
    gamestate.key[13]=225;
    gamestate.key[14]=225;
    gamestate.key[15]=193;

    memcpy(gamestate.second_flag,arr2,24);

	memset(res,0,64);

	rc2_cc_set_key(&cx,gamestate.key,16);
	for (int i=0;i<24;i=i+8) {
		rc2_cc_decrypt(&cx, gamestate.second_flag+i, res+i);
	}
	puts(res);

    return 0;
}
