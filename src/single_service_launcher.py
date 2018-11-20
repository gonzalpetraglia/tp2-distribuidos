import importlib
import sys
END_TOKEN = 'END'
if __name__ == '__main__':
    
    if (len(sys.argv) < 3):
        print ("Usage python single_service_launcher.py <module_name> <process_class> [arg1 arg2 arg3 ...]")
    module = importlib.__import__(sys.argv[1], fromlist=[sys.argv[2]])
    ProcessClass = getattr(module, sys.argv[2])

    process = ProcessClass(*(sys.argv[3:]))

    process.run()