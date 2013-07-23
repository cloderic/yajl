include(CMakeDependentOption)
CMAKE_DEPENDENT_OPTION(IOS "Enable iOS builds" 
    OFF "APPLE"
    OFF)

CMAKE_DEPENDENT_OPTION(IOS_SIMULATOR "Enable iOS simulator build (won't work on devices)" 
    ON "IOS"
    OFF)

if(IOS)
    set(CMAKE_OSX_SYSROOT iphoneos6.1) #Should be configured or retrieved using a find.
    set(IOS_VERSION_MAJOR 6) #idem
    set(IOS_VERSION_MINOR 1) #idem
    
    if(IOS_SIMULATOR)
        # building for the simulator
        set(IOS_PLATFORM "iphonesimulator")
        set(CMAKE_OSX_ARCHITECTURES "i386")
    else()
        # building to the device
        set(IOS_PLATFORM "iphoneos")
        set(CMAKE_OSX_ARCHITECTURES "armv6;armv7;armv7s") #Should be configured or retrieved using a find.
    endif()
    set(CMAKE_XCODE_EFFECTIVE_PLATFORMS "-${IOS_PLATFORM}")
endif()