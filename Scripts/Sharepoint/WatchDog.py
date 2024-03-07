from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import PopulateCC1

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.split('.')[-1] == 'xlsx':
            # print("New file created:", event.src_path.split('/')[-1], event.event_type)
            print(f"Calling CC1.main on {event.src_path.split('/')[-1]}")
            PopulateCC1.main('/Users/ruben/PycharmProjects/PDFExtract/venv/files/Sharepoint/',event.src_path)
            print("CC1 Completed")
        if event.is_directory:
            print("New folder created:", event.src_path.split('/')[-1])
        # print(event)

    # def on_modified(self, event):
    #     if not event.is_directory:
    #         print("New file created:", event.src_path.split('/')[-1], event.event_type)
    #     if event.is_directory:
    #         print("New folder created:", event.src_path.split('/')[-1])
    #     print(event)

if __name__ == "__main__":
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path='/Users/ruben/PycharmProjects/PDFExtract/venv/files/Sharepoint/', recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()