/**
 * @author behrang
 * @file
 * @date Dec 20, 2015
 * @details Detects the operation system and defines according preprocessor symbols
 */

#ifndef _OS_DETECTION_
#define _OS_DETECTION_

#if defined(_MSC_VER)
#define DLL_EXPORT extern "C" __declspec(dllexport)
#else
#define DLL_EXPORT extern "C"
#endif

#endif
