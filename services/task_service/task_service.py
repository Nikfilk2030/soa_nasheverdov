import threading
from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToDict

import services.proto.service_pb2 as service_pb2
import services.proto.service_pb2_grpc as service_pb2_grpc
import services.task_service.database as database


class EStatus:
    ERROR = 228
    SUCCESS = 1337


class TaskService(service_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        self._lock = threading.Lock()

    def CreateTask(self, request, context):
        with self._lock:
            request_dict = MessageToDict(request)
            success = database.create_task(
                task_id=request_dict['id'],
                username=request_dict['username'],
                content=request_dict['content'],
                date=request_dict['date'],
                tag=request_dict['tag']
            )
            if success:
                return service_pb2.TaskResponse(status=EStatus.SUCCESS, task=request)
            else:
                return service_pb2.TaskResponse(status=EStatus.ERROR, task=service_pb2.Task())

    def UpdateTask(self, request, context):
        with self._lock:
            request_dict = MessageToDict(request)
            success = database.update_task(
                task_id=request_dict['id'],
                content=request_dict['content'],
                date=request_dict['date'],
                tag=request_dict['tag']
            )
            if success:
                return service_pb2.TaskResponse(status=EStatus.SUCCESS, task=request)
            else:
                return service_pb2.TaskResponse(status=EStatus.ERROR, task=service_pb2.Task())

    def DeleteTask(self, request, context):
        with self._lock:
            request_dict = MessageToDict(request)
            success = database.delete_task(task_id=request_dict['id'])
            return service_pb2.DeleteResponse(success=success)

    def GetTaskByID(self, request, context):
        with self._lock:
            request_dict = MessageToDict(request)
            success, task = database.get_task_by_id(task_id=request_dict['id'])
            if success:
                return service_pb2.TaskResponse(status=EStatus.SUCCESS, task=task)
            else:
                return service_pb2.TaskResponse(status=EStatus.ERROR, task=service_pb2.Task())

    def GetTasks(self, request, context):
        with self._lock:
            request_dict = MessageToDict(request)

            page_number = int(request_dict['pageNumber'])
            page_size = int(request_dict['pageSize'])

            tasks = database.get_tasks(page_number=page_number, page_size=page_size)
            return tasks


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    service_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('0.0.0.0:51075')
    server.start()
    server.wait_for_termination(timeout=None)


if __name__ == '__main__':
    serve()
