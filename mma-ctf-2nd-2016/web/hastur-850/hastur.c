#include "php.h"
#include "ext/standard/info.h"

#include "zend_alloc.h"
#include "zend_API.h"

//#define DEBUG

static PHP_MINFO_FUNCTION(hastur);
static PHP_RINIT_FUNCTION(hastur);
static PHP_FUNCTION(hastur_set_handler);
static PHP_FUNCTION(hastur_set_name);
static PHP_FUNCTION(hastur_ia_ia_handler);
static PHP_FUNCTION(hastur_ia_ia);
#ifdef DEBUG
static PHP_FUNCTION(hastur_dump);
#endif

ZEND_BEGIN_ARG_INFO(arginfo_hastur_ia_ia, 0)
ZEND_ARG_INFO(0, text)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO(arginfo_hastur_ia_ia_handler, 0)
ZEND_ARG_INFO(0, text)
ZEND_ARG_INFO(0, name)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO(arginfo_hastur_set_handler, 0)
ZEND_ARG_INFO(0, func_name)
ZEND_END_ARG_INFO()

ZEND_BEGIN_ARG_INFO(arginfo_hastur_set_name, 0)
ZEND_ARG_INFO(0, name)
ZEND_END_ARG_INFO()

#ifdef DEBUG
ZEND_BEGIN_ARG_INFO(arginfo_hastur_dump, 0)
ZEND_ARG_INFO(0, var)
ZEND_END_ARG_INFO()
#endif

static const zend_function_entry hastur_functions[] = {
    PHP_FE(hastur_set_name, arginfo_hastur_set_name)
    PHP_FE(hastur_set_handler, arginfo_hastur_set_handler)
    PHP_FE(hastur_ia_ia_handler, arginfo_hastur_ia_ia_handler)
    PHP_FE(hastur_ia_ia, arginfo_hastur_ia_ia)
#ifdef DEBUG
    PHP_FE(hastur_dump, arginfo_hastur_dump)
#endif
    PHP_FE_END
};

zend_module_entry hastur_module_entry = {
    STANDARD_MODULE_HEADER,
    "hastur",
    hastur_functions,
    NULL,
    NULL,
    PHP_RINIT(hastur),
    NULL,
    PHP_MINFO(hastur),
    NO_VERSION_YET,
    STANDARD_MODULE_PROPERTIES
};
ZEND_GET_MODULE(hastur)

static PHP_MINFO_FUNCTION(hastur)
{
    php_info_print_table_start();
    php_info_print_table_row(2, "hastur", "enabled");
    php_info_print_table_end();
}

static char handler[32]; // = "hastur_ia_ia_handler";
static char god_name[32]; // = "Hastur";

static PHP_RINIT_FUNCTION(hastur) {
    strncpy(god_name, "Hastur", strlen("Hastur") + 1);
    strncpy(handler, "hastur_ia_ia_handler", strlen("hastur_ia_ia_handler") + 1);
}

static PHP_FUNCTION(hastur_set_name)
{
    char *str;
    int str_len;

    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "s", &str, &str_len) == FAILURE) {
        return;
    }

    strncpy(god_name, str, str_len + 1);
}

static PHP_FUNCTION(hastur_set_handler)
{
    char *str;
    int str_len;

    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "s", &str, &str_len) == FAILURE) {
        return;
    }

    strncpy(handler, str, str_len + 1);
}

static PHP_FUNCTION(hastur_ia_ia)
{
    zval **params[2];
    char *text;
    int text_len;
    zval *text_zval;
    zval *name_zval;
    zval *handler_zval;
    zval *retval_ptr;
    int i;

    MAKE_STD_ZVAL(handler_zval);
    MAKE_STD_ZVAL(name_zval);
    MAKE_STD_ZVAL(text_zval);
    ZVAL_STRING(handler_zval, handler, 1);
    ZVAL_STRING(name_zval, god_name, 1);
    params[0] = &text_zval;
    params[1] = &name_zval;

    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "s", &text, &text_len) == FAILURE) {
        RETURN_FALSE;
    }
    ZVAL_STRINGL(text_zval, text, text_len, 1);
    char *ntext = Z_STRVAL_P(text_zval);
    for (i = 0; i < text_len; i++) {
        if (strncmp(ntext + i, "flag", 4) == 0) {
            strncpy(ntext + i, "iaia", 4);
        }
    }

    if (call_user_function_ex(EG(function_table), NULL, handler_zval,
                              &retval_ptr, 2, params, 0, NULL TSRMLS_CC) == SUCCESS) {
        if (retval_ptr) {
            COPY_PZVAL_TO_ZVAL(*return_value, retval_ptr);
        }
    }

    FREE_ZVAL(handler_zval);
    FREE_ZVAL(name_zval);
}

static PHP_FUNCTION(hastur_ia_ia_handler)
{
    char *text, *name;
    int text_len, name_len;
    int i;
    char extra[1024];
    int extra_len;

    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "ss",
                              &text, &text_len,
                              &name, &name_len) == FAILURE) {
        RETURN_FALSE;
    }

    snprintf(extra, sizeof(extra), " ia! ia! %s!", name);
    extra_len = strlen(extra);

    size_t new_len = 0;
    char *p = text;
    while (*p) {
        new_len++;
        if (*p++ == '.')
            new_len += extra_len;
    }

    char *ns = emalloc(new_len + 1);
    p = ns;
    for (i = 0; i < text_len; i++) {
        *p++ = text[i];
        if (text[i] == '.') {
            strncpy(p, extra, extra_len);
            p += extra_len;
        }
    }
    *p = '\0';
    RETURN_STRING(ns, 0);
}

#ifdef DEBUG
static PHP_FUNCTION(hastur_dump)
{
    zval *var;
    char buf[1024];
    int i, j;

    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "z", &var) == FAILURE) {
        RETURN_FALSE;
    }
    
    sprintf(buf, "zval: %p\n  type: %d\n", var, var->type);
    php_output_write(buf, strlen(buf));

    switch (var->type) {
    case IS_STRING:
        sprintf(buf, "  val: %p", var->value.str.val);
        php_output_write(buf, strlen(buf));

        for (i = 0; i < 512; i++) {
            if (i % 16 == 0) {
                php_output_write("\n", 1);
                sprintf(buf, "%08lx: ", (long)var->value.str.val + i - 16);
                php_output_write(buf, strlen(buf));
            }
            sprintf(buf, "%02x ", (unsigned char)var->value.str.val[i-16]);
            php_output_write(buf, strlen(buf));
        }
        php_output_write("\n", 1);
        break;
    default:
        sprintf(buf, "  other type\n");
        php_output_write(buf, strlen(buf));
        break;
    }
}
#endif

