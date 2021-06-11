#include <stdlib.h>
#include <string.h>

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1;

typedef sqlite3_int64 i64;

static void encrypt_Caesar(sqlite3_context *context, int argc,
                           sqlite3_value **argv) {
    if (argc == 2) {
        char *text = (char *)sqlite3_value_text(argv[0]);
        int key = atoi((char *)sqlite3_value_text(argv[1]));
        if (text && text[0]) {
            int n = strlen(text);
            char result[n + 1];
            for (int i = 0; i < n; i++) {
                // result[i] = text[i] + key;
                result[i] = ((text[i] - 33 + key) % 93 + 93) % 93 + 33;
            }
            result[n] = '\0';
            sqlite3_result_text(context, result, -1, SQLITE_TRANSIENT);
            return;
        }
    }
    sqlite3_result_null(context);
}

static void decrypt_Caesar(sqlite3_context *context, int argc,
                           sqlite3_value **argv) {
    if (argc == 2) {
        char *text = (char *)sqlite3_value_text(argv[0]);
        int key = atoi((char *)sqlite3_value_text(argv[1]));
        if (text && text[0]) {
            int n = strlen(text);
            char result[n + 1];
            for (int i = 0; i < n; i++) {
                // result[i] = text[i] - key;
                result[i] = ((text[i] - 33 - key) % 93 + 93) % 93 + 33;
            }
            result[n] = '\0';
            sqlite3_result_text(context, result, -1, SQLITE_TRANSIENT);
            return;
        }
    }
    sqlite3_result_null(context);
}

int sqlite3_extension_init(sqlite3 *db, char **err,
                           const sqlite3_api_routines *api) {
    SQLITE_EXTENSION_INIT2(api);

    sqlite3_create_function(db, "encrypt_Caesar", 2, SQLITE_UTF8, NULL,
                            encrypt_Caesar, NULL, NULL);

    sqlite3_create_function(db, "decrypt_Caesar", 2, SQLITE_UTF8, NULL,
                            decrypt_Caesar, NULL, NULL);

    return 0;
}
