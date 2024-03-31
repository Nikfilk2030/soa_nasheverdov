import grpc

from concurrent import futures

import services.proto.service_pb2_grpc as service_pb2_grpc
import services.proto.service_pb2 as service_pb2


class TaskService(service_pb2_grpc.TaskServiceServicer):

    def CreateTask(self, request, context):
        print('bebra')
        # Authentication and implement the logic to create a task
        # INSERT INTO tasks (id, title, description, user_id) VALUES (?, ?, ?, ?)
        return service_pb2.TaskResponse(status=228, task=request)

    def UpdateTask(self, request, context):
        # Authentication and implement the logic to update a task
        # UPDATE tasks SET title=?, description=? WHERE id=? AND user_id=?
        return service_pb2.TaskResponse(task=request)

    def DeleteTask(self, request, context):
        # Authentication and implement the logic to delete a task
        # DELETE FROM tasks WHERE id=? AND user_id=?
        return service_pb2.DeleteResponse(success=True)

    def GetTaskByID(self, request, context):
        # Authentication and implement the logic to get a task by ID
        # SELECT * FROM tasks WHERE id=? AND user_id=?
        return service_pb2.Task(id=request.id, title="Sample Title", description="Sample Description",
                                user_id="User123")

    def GetTasksWithPagination(self, request, context):
        # Implement the logic to get a list of tasks with pagination
        # SELECT * FROM tasks LIMIT ? OFFSET ?
        task_list = service_pb2.TaskList()
        # Your code to populate task_list
        return task_list


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
