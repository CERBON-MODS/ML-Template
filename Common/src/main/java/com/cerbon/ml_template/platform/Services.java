package com.cerbon.ml_template.platform;

import com.cerbon.ml_template.ModName;

import java.util.ServiceLoader;

public class Services {

    public static <T> T load(Class<T> clazz) {
        final T loadedService = ServiceLoader.load(clazz)
                .findFirst()
                .orElseThrow(() -> new NullPointerException("Failed to load service for " + clazz.getName()));
        ModName.LOGGER.debug("Loaded {} for service {}", loadedService, clazz);
        return loadedService;
    }
}
