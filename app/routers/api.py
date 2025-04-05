from app.utils.auth import get_storage_for_api
from app.utils.storage import ReminderList, ReminderItem, ReminderStorage

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional

router = APIRouter(
  prefix="/api",
  tags=["API"]
)


class NewReminderListName(BaseModel):
  name: str


class NewReminderItem(BaseModel):
  description: str


class SelectedListId(BaseModel):
  list_id: Optional[int]


@router.get(
  path="/reminders",
  summary="Get the user's reminder lists",
  response_model=List[ReminderList]
)
async def get_reminders(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> list[ReminderList]:

  return storage.get_lists()


@router.post(
  path="/reminders",
  summary="Create a new reminder list",
  response_model=ReminderList
)
async def post_reminders(
  reminder_list: NewReminderListName,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:

  list_id = storage.create_list(reminder_list.name)
  return storage.get_list(list_id)


@router.get(
  path="/reminders/{list_id}",
  summary="Get a reminder list by ID",
  response_model=ReminderList
)
async def get_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:

  return storage.get_list(list_id)


@router.patch(
  path="/reminders/{list_id}",
  summary="Updates a reminder list's name",
  response_model=ReminderList
)
async def patch_list_id(
  list_id: int,
  reminder_list: NewReminderListName,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderList:
  
  storage.update_list_name(list_id, reminder_list.name)
  return storage.get_list(list_id)


@router.delete(
  path="/reminders/{list_id}",
  summary="Deletes a reminder list",
  response_model=dict
)
async def delete_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.delete_list(list_id)
  return dict()


@router.get(
  path="/reminders/{list_id}/items",
  summary="Get all reminder items for a list",
  response_model=List[ReminderItem]
)
async def get_list_id_items(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> List[ReminderItem]:

  return storage.get_items(list_id)


@router.post(
  path="/reminders/{list_id}/items",
  summary="Add a new item to a reminder list",
  response_model=ReminderItem
)
async def post_reminders_list_id_items(
  list_id: int,
  reminder_item: NewReminderItem,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:

  item_id = storage.add_item(list_id, reminder_item.description)
  return storage.get_item(item_id)


@router.get(
  path="/reminders/items/{item_id}",
  summary="Get a reminder item by ID",
  response_model=ReminderItem
)
async def get_items_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:

  return storage.get_item(item_id)


@router.patch(
  path="/reminders/items/{item_id}",
  summary="Update a reminder item's description",
  response_model=ReminderItem
)
async def patch_items_item_id(
  item_id: int,
  reminder_item: NewReminderItem,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  
  storage.update_item_description(item_id, reminder_item.description)
  return storage.get_item(item_id)


@router.patch(
  path="/reminders/items/strike/{item_id}",
  summary="Toggle the completed status of a reminder item",
  response_model=ReminderItem
)
async def patch_items_strike_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> ReminderItem:
  
  storage.strike_item(item_id)
  return storage.get_item(item_id)


@router.delete(
  path="/reminders/items/{item_id}",
  summary="Deletes a reminder item",
  response_model=Dict
)
async def delete_items_item_id(
  item_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.delete_item(item_id)
  return dict()


@router.get(
  path="/reminders/selected",
  summary="Get the selected reminder list",
  response_model=SelectedListId
)
async def get_selected(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> SelectedListId:

  list_id = storage.get_selected_list_id()
  return SelectedListId(list_id=list_id)


@router.post(
  path="/reminders/select/{list_id}",
  summary="Select a reminder list",
  response_model=Dict
)
async def post_select_list_id(
  list_id: int,
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.set_selected_list(list_id)
  return {}


@router.post(
  path="/reminders/unselect",
  summary="Unselect any reminder list",
  response_model=Dict
)
async def post_unselect(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.set_selected_list(None)
  return {}


@router.delete(
  path="/reminders/delete-lists",
  summary="Delete all the user's reminder lists",
  response_model=Dict
)
async def delete_delete_lists(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.delete_lists()
  return {}


@router.post(
  path="/reminders/create-new-lists",
  summary="Create an entirely new set of reminders after deleting old reminders",
  response_model=Dict
)
async def post_create_new_lists(
  storage: ReminderStorage = Depends(get_storage_for_api)
) -> Dict:

  storage.delete_lists()

  # Chores
  chores_id = storage.create_list("Chores")
  storage.set_selected_list(chores_id)
  storage.add_item(chores_id, "")
  storage.add_item(chores_id, "")
  storage.strike_item(storage.add_item(chores_id, ""))
  storage.strike_item(storage.add_item(chores_id, ""))
  storage.add_item(chores_id, "")

  # Groceries
  groceries_id = storage.create_list("")
  storage.add_item(groceries_id, "")
  storage.add_item(groceries_id, "")
  storage.add_item(groceries_id, "")
  storage.add_item(groceries_id, "")
  storage.add_item(groceries_id, "")
  storage.add_item(groceries_id, "")

  # Projects
  projects_id = storage.create_list("")
  storage.strike_item(storage.add_item(projects_id, ""))
  storage.add_item(projects_id, "")
  storage.add_item(projects_id, "")

  return {}
