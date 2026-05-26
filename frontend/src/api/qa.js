import request from "../utils/request";

export const sendMessage = (data) => {
  return request({
    url: "/qa/chat",
    method: "post",
    data,
  });
};

export const getConversations = (params) => {
  return request({
    url: "/qa/conversations",
    method: "get",
    params,
  });
};

export const getConversation = (conversationId) => {
  return request({
    url: `/qa/conversation/${conversationId}`,
    method: "get",
  });
};

export const updateConversation = (conversationId, title) => {
  return request({
    url: `/qa/conversation/${conversationId}`,
    method: "put",
    params: { title },
  });
};

export const deleteConversation = (conversationId) => {
  return request({
    url: `/qa/conversation/${conversationId}`,
    method: "delete",
  });
};