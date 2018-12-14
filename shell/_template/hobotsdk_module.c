 
//
// Created by %user%@hobot.cc on %date%.
// Copyright (c) %year% horizon robotics. All rights reserved.
//

#include "hobot_c/hobot_c.h"
#include "hobot_c/logging.h"
#include "%mod%.h"


module_t *%mod%_new(char *instance_name)
{
    module_t *m = module_new();
    module_set_name(m, instance_name);
    module_set_initialize(m, %mod%_init);

    // set data if need
    //module_set_data(m, %mod%_data);
    module_add_forward(m, %mod%_forward_0, 0);
    return m;
}

int %mod%_init(context_t *c, module_t *%mod%)
{
    log(INFO, "%s init", module_get_name(%mod%));
    return 0;
}

void %mod%_forward_0(context_t *c, 
                    module_t *%mod%, 
                    int forward_index, 
                    const vector_t *inputs)
{
    // TODO
}

void %mod%_free(module_t *%mod%)
{
    free(%mod%);

}
