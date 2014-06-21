-----------------------------------------------------------------------------------------------
-- Client Lua Script for <WSNAME>
-- Copyright (c) NCsoft. All rights reserved
-----------------------------------------------------------------------------------------------
 
require "Window"
 
-----------------------------------------------------------------------------------------------
-- <WSNAME> Module Definition
-----------------------------------------------------------------------------------------------
local <WSNAME> = {} 
 
-----------------------------------------------------------------------------------------------
-- Constants
-----------------------------------------------------------------------------------------------
-- e.g. local kiExampleVariableMax = 999
<IFLIST>local kcrSelectedText = ApolloColor.new("UI_BtnTextHoloPressedFlyby")
<IFLIST>local kcrNormalText = ApolloColor.new("UI_BtnTextHoloNormal")
 
-----------------------------------------------------------------------------------------------
-- Initialization
-----------------------------------------------------------------------------------------------
function <WSNAME>:new(o)
    o = o or {}
    setmetatable(o, self)
    self.__index = self 

    -- initialize variables here
<IFLIST>    o.tItems = {} -- keep track of all the list items
<IFLIST>    o.wndSelectedListItem = nil -- keep track of which list item is currently selected

    return o
end

function <WSNAME>:Init()
    local bHasConfigureFunction = false
    local strConfigureButtonText = ""
    local tDependencies = {
        -- "UnitOrPackageName",
    }
    Apollo.RegisterAddon(self, bHasConfigureFunction, strConfigureButtonText, tDependencies)
end
 

-----------------------------------------------------------------------------------------------
-- <WSNAME> OnLoad
-----------------------------------------------------------------------------------------------
function <WSNAME>:OnLoad()
    -- load our form file
    self.xmlDoc = XmlDoc.CreateFromFile("<WSNAME>.xml")
    self.xmlDoc:RegisterCallback("OnDocLoaded", self)
end

-----------------------------------------------------------------------------------------------
-- <WSNAME> OnDocLoaded
-----------------------------------------------------------------------------------------------
function <WSNAME>:OnDocLoaded()

    if self.xmlDoc ~= nil and self.xmlDoc:IsLoaded() then
        self.wndMain = Apollo.LoadForm(self.xmlDoc, "<WSNAME>Form", nil, self)
        if self.wndMain == nil then
            Apollo.AddAddonErrorText(self, "Could not load the main window for some reason.")
            return
        end
        
<IFLIST>        -- item list
<IFLIST>        self.wndItemList = self.wndMain:FindChild("ItemList")
        self.wndMain:Show(false, true)

        -- if the xmlDoc is no longer needed, you should set it to nil
        -- self.xmlDoc = nil
        
        -- Register handlers for events, slash commands and timer, etc.
        -- e.g. Apollo.RegisterEventHandler("KeyDown", "OnKeyDown", self)
<IFCMD>        Apollo.RegisterSlashCommand("<WSCMD>", "On<WSNAME>On", self)

<IFTIMER>        self.timer = ApolloTimer.Create(<WSTIMER>, <WSREPEAT>, "OnTimer", self)

        -- Do additional Addon initialization here
    end
end

-----------------------------------------------------------------------------------------------
-- <WSNAME> Functions
-----------------------------------------------------------------------------------------------
-- Define general functions here

<IFCMD>-- on SlashCommand "/<WSCMD>"
<IFCMD>function <WSNAME>:On<WSNAME>On()
<IFCMD>    self.wndMain:Invoke() -- show the window
<IFCMD><IFLIST>    
<IFCMD><IFLIST>    -- populate the item list
<IFCMD><IFLIST>    self:PopulateItemList()
<IFCMD>end

<IFTIMER>-- on timer
<IFTIMER>function <WSNAME>:OnTimer()
<IFTIMER>    -- Do your timer-related stuff here.
<IFTIMER>end
<IFTIMER>

-----------------------------------------------------------------------------------------------
-- <WSNAME>Form Functions
-----------------------------------------------------------------------------------------------
-- when the OK button is clicked
function <WSNAME>:OnOK()
    self.wndMain:Close() -- hide the window
end

-- when the Cancel button is clicked
function <WSNAME>:OnCancel()
    self.wndMain:Close() -- hide the window
end

<IFLIST>
<IFLIST>-----------------------------------------------------------------------------------------------
<IFLIST>-- ItemList Functions
<IFLIST>-----------------------------------------------------------------------------------------------
<IFLIST>-- populate item list
<IFLIST>function <WSNAME>:PopulateItemList()
<IFLIST>    -- make sure the item list is empty to start with
<IFLIST>    self:DestroyItemList()
<IFLIST>    
<IFLIST>    -- add 20 items
<IFLIST>    for i = 1,20 do
<IFLIST>        self:AddItem(i)
<IFLIST>    end
<IFLIST>    
<IFLIST>    -- now all the item are added, call ArrangeChildrenVert to list out the list items vertically
<IFLIST>    self.wndItemList:ArrangeChildrenVert()
<IFLIST>end
<IFLIST>
<IFLIST>-- clear the item list
<IFLIST>function <WSNAME>:DestroyItemList()
<IFLIST>    -- destroy all the wnd inside the list
<IFLIST>    for idx,wnd in ipairs(self.tItems) do
<IFLIST>        wnd:Destroy()
<IFLIST>    end
<IFLIST>
<IFLIST>    -- clear the list item array
<IFLIST>    self.tItems = {}
<IFLIST>    self.wndSelectedListItem = nil
<IFLIST>end
<IFLIST>
<IFLIST>-- add an item into the item list
<IFLIST>function <WSNAME>:AddItem(i)
<IFLIST>    -- load the window item for the list item
<IFLIST>    local wnd = Apollo.LoadForm(self.xmlDoc, "ListItem", self.wndItemList, self)
<IFLIST>    
<IFLIST>    -- keep track of the window item created
<IFLIST>    self.tItems[i] = wnd
<IFLIST>
<IFLIST>    -- give it a piece of data to refer to 
<IFLIST>    local wndItemText = wnd:FindChild("Text")
<IFLIST>    if wndItemText then -- make sure the text wnd exist
<IFLIST>        wndItemText:SetText("item " .. i) -- set the item wnd's text to "item i"
<IFLIST>        wndItemText:SetTextColor(kcrNormalText)
<IFLIST>    end
<IFLIST>    wnd:SetData(i)
<IFLIST>end
<IFLIST>
<IFLIST>-- when a list item is selected
<IFLIST>function <WSNAME>:OnListItemSelected(wndHandler, wndControl)
<IFLIST>    -- make sure the wndControl is valid
<IFLIST>    if wndHandler ~= wndControl then
<IFLIST>        return
<IFLIST>    end
<IFLIST>    
<IFLIST>    -- change the old item's text color back to normal color
<IFLIST>    local wndItemText
<IFLIST>    if self.wndSelectedListItem ~= nil then
<IFLIST>        wndItemText = self.wndSelectedListItem:FindChild("Text")
<IFLIST>        wndItemText:SetTextColor(kcrNormalText)
<IFLIST>    end
<IFLIST>    
<IFLIST>    -- wndControl is the item selected - change its color to selected
<IFLIST>    self.wndSelectedListItem = wndControl
<IFLIST>    wndItemText = self.wndSelectedListItem:FindChild("Text")
<IFLIST>    wndItemText:SetTextColor(kcrSelectedText)
<IFLIST>    
<IFLIST>    Print( "item " ..  self.wndSelectedListItem:GetData() .. " is selected.")
<IFLIST>end
<IFLIST>

-----------------------------------------------------------------------------------------------
-- <WSNAME> Instance
-----------------------------------------------------------------------------------------------
local <WSNAME>Inst = <WSNAME>:new()
<WSNAME>Inst:Init()
