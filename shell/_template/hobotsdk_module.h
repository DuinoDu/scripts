 
//
// Created by %user%@hobot.cc on %date%.
// Copyright (c) %year% horizon robotics. All rights reserved.
//

#ifndef __%MOD%_H__
#define __%MOD%_H__

#include "hobot_c/hobot_c.h"

module_t *%mod%_new(char *instance_name);

int %mod%_init(context_t *c, module_t *%mod%);

void %mod%_forward_0(context_t *c, module_t *%mod%, int forward_index, const vector_t *inputs);

void %mod%_free(module_t *%mod%);

#endif
