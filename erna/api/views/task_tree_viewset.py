from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from rna_seq.models import Task, TaskTree, MethodRelation
from api.serializers import *

class TaskTreeViewSet(viewsets.ModelViewSet):
    queryset = TaskTree.objects.all()
    serializer_class = TaskTreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def update_task_parents(self, request):
        project_id = request.data.get('project_id')
        child_task_id = request.data.get('child')
        parent_ids = request.data.get('parents')
        res = []
        if project_id and child_task_id:
            child_task, tree = TaskTree.objects.get_parents(project_id, child_task_id)
            # remove relation if needed
            for tree_parent in tree:
                # omit it if the parent is existing
                if tree_parent.parent.task_id in parent_ids:
                    parent_ids.remove(tree_parent.parent.task_id)
                else:
                    # delete this task relation
                    tree_parent.delete()
            # add new relations
            for parent_task_id in parent_ids:
                parent_task = Task.objects.get(project_id=project_id, task_id=parent_task_id)
                obj = TaskTree.objects.create(parent=parent_task, child=child_task)
                print(obj)
            # get new parents
            _, new_tree = TaskTree.objects.get_parents(project_id, child_task_id)
            res = [task_tree.parent.task_id for task_tree in new_tree]
            print(res)
        return Response(res)

